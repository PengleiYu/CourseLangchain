from utils.qdrant_helper import QdrantHelper
from langchain.schema import Document

helper = QdrantHelper()
qdrant = helper.create_vectorstore('./OneFlower')

result: list[Document] = qdrant.similarity_search('总经理说了什么')
for d in result:
    print(d)

# MultiRetrievalQAChain()
