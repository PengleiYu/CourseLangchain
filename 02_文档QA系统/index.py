# 手动实现RAG
import os

# 1. 加载文档
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.schema import Document

base_dir = './docs'
documents: list[Document] = []

for file in os.listdir(base_dir):
    file_path = os.path.join(base_dir, file)
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.doc') or file.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        loader = TextLoader(file_path)
        documents.extend(loader.load())

# 2. 分割文档
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

# 3. 嵌入并存储到db
from langchain.vectorstores.qdrant import Qdrant
from langchain.embeddings import OpenAIEmbeddings

vectorstore = Qdrant.from_documents(documents=chunked_documents,
                                    embedding=OpenAIEmbeddings(),
                                    location=':memory:',
                                    collection_name='my_documents', )
# 4. 准备查询对象
import logging
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA

logging.basicConfig()
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever_from_llm)

# flask
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question = request.form.get('question')
        result = qa_chain({'query': question})
    else:
        result = {'result': '这里将会展示答案'}
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    print('http://localhost:5000')
