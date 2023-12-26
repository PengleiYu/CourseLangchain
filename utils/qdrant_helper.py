import os
from typing import Optional

from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionDescription

COLLECTION_NAME_DEFAULT = "my_documents"
VECTORSTORE_DEFAULT_PATH = "./db"


class QdrantHelper:
    vectorstore_path: str
    collection_name: str

    def __init__(self,
                 vectorstore_path: str = VECTORSTORE_DEFAULT_PATH,
                 collection_name: str = COLLECTION_NAME_DEFAULT,
                 ) -> None:
        super().__init__()
        self.vectorstore_path = vectorstore_path
        self.collection_name = collection_name

    def create_vectorstore(self, base_dir: str) -> Qdrant:
        _qdrant: Optional[Qdrant] = self.create_vs_from_exist()
        if not _qdrant:
            _qdrant = self.create_vs_from_docs(base_dir)
        return _qdrant

    def create_vs_from_docs(self, base_dir: str) -> Qdrant:
        print(f'create vectorstore from docs: base_dir = {base_dir}')
        documents = []
        loader: Optional[BaseLoader] = None
        for file in os.listdir(base_dir):
            file_path = os.path.join(base_dir, file)
            if file.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif file.endswith('.docx') or file.endswith('.doc'):
                loader = Docx2txtLoader(file_path)
            elif file.endswith('.txt'):
                loader = TextLoader(file_path)
            if loader is not None:
                documents.extend(loader.load())
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        split_documents = splitter.split_documents(documents)
        return Qdrant.from_documents(
            documents=split_documents,
            embedding=OpenAIEmbeddings(),
            path=self.vectorstore_path,
            collection_name=self.collection_name,
        )

    def create_vs_from_exist(self) -> Optional[Qdrant]:
        print(f'create_vs_from_exist: ')
        # path表示本地路径，location表示网络路径
        client = QdrantClient(path=self.vectorstore_path)
        collections: list[CollectionDescription] = client.get_collections().collections
        if not collections:
            return None
        my_collection = next((col for col in collections if col.name == self.collection_name), None, )
        if not my_collection:
            return None

        return Qdrant(
            client=client,
            collection_name=self.collection_name,
            embeddings=OpenAIEmbeddings(),
        )
