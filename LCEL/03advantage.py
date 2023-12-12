import asyncio
import os
from typing import List

from langchain.schema.runnable import RunnablePassthrough, RunnableConfig
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser, Document
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough, ConfigurableField
from langchain.schema.runnable.configurable import DynamicRunnable
from langchain.vectorstores.qdrant import Qdrant
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatAnthropic

prompt = ChatPromptTemplate.from_template('给我讲个关于{topic}的的笑话')
output_parser = StrOutputParser()
model = ChatOpenAI()
llm = OpenAI(model="gpt-3.5-turbo-instruct")
# anthropic = ChatAnthropic(model="claude-2")

chain = {"topic": RunnablePassthrough()} | prompt | model | output_parser

user_input = '香蕉'

# 1. 直接执行
# result: str = chain.invoke('香蕉')
# print(result)

# 2. stream
# for chunk in chain.stream(user_input):
#     print(chunk, end='', flush=True)

# 3. batch
# batch_result: list[str] = chain.batch(inputs=['香蕉', '苹果', '橘子'])
# print(batch_result)

# 4. async
# async def a_invoke():
#     result: str = await chain.ainvoke(input=user_input)
#     print(result)
#
#
# asyncio.run(a_invoke())

# 5. 替换model
# chain2 = {'topic': RunnablePassthrough()} | prompt | llm | output_parser
# result: str = chain2.invoke(input=user_input)
# print(result)

# 6. 替换model厂商
# anthropic_chain = (
#         {"topic": RunnablePassthrough()}
#         | prompt
#         | anthropic
#         | output_parser
# )
# print(anthropic_chain.invoke(input=user_input))

# 7. 运行时配置
# configurable_model = model.configurable_alternatives(
#     which=ConfigurableField(id='model'),
#     default_key='chat_openai',
#     openai=llm,
#     anthropic=anthropic,
# )
# configurable_chain = {'topic': RunnablePassthrough()} | prompt | configurable_model | output_parser
#
# print(configurable_chain.invoke(
#     input=user_input,
#     config=RunnableConfig(
#         configurable={"model": "openai"}))
# )

# 8. langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
result: str = chain.invoke('香蕉')
print(result)
