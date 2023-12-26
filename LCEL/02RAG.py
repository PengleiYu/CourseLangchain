from typing import Dict, Union, List, Any

from langchain.callbacks.base import BaseCallbackHandler, BaseCallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser, Document
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough, RunnableConfig
from langchain.vectorstores.qdrant import Qdrant

from utils.callback_handler import MyBaseCallbackHandler

question = "where did harrison work?"

retriever = Qdrant.from_texts(
    texts=["harrison worked at kensho", "bears like to eat honey"],
    location=":memory:",
    embedding=OpenAIEmbeddings(),
).as_retriever()
result_retriever: list[Document] = retriever.invoke(question)
print(result_retriever)

prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context:
{context}

Question: {question}
""")

model = ChatOpenAI()
output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough(),
})

chain = setup_and_retrieval | prompt | model | output_parser

result: str = chain.invoke(question, config={"callbacks": [MyBaseCallbackHandler()]})
print(result)
