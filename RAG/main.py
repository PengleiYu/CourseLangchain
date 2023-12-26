from langchain.chains import RetrievalQA
from langchain.llms.openai import OpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever

from utils.qdrant_helper import QdrantHelper

doc_dir = '../02_文档QA系统/docs'
qdrant = QdrantHelper().create_vectorstore(base_dir=doc_dir)
llm = OpenAI()
query_retriever = MultiQueryRetriever.from_llm(retriever=(qdrant.as_retriever()), llm=llm, )
qa = RetrievalQA.from_chain_type(llm=llm, retriever=query_retriever)
question = "请简述公司的规范"
result = qa.run(question)
print(result)
