from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import PromptValue, BaseMessage, AIMessage
from langchain.schema.output_parser import StrOutputParser

input_dict = {'topic': '冰淇淋'}

prompt = ChatPromptTemplate.from_template("给我讲个关于{topic}笑话")
# prompt_value: PromptValue = prompt.invoke(input_dict)
# print(prompt_value)
# print(prompt_value.to_string())

model = ChatOpenAI()
# message: BaseMessage = model.invoke(input=prompt_value)
# print(message)

output_parser = StrOutputParser()
# output: str = output_parser.invoke(message)
# print(output)

# chain = prompt | model | output_parser

# result = chain.invoke(input_dict)
# print(result)


message: AIMessage = (prompt | model).invoke(input_dict)
print(message)
