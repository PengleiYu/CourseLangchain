import os
from typing import Optional

from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.qdrant import Qdrant


class CommandlineChatbot:
    messages: [BaseMessage] = []

    def __init__(self) -> None:
        super().__init__()
        self.llm = ChatOpenAI(verbose=True, model_name='gpt-4-1106-preview', )
        self.messages.append(SystemMessage(content="你是一个花卉行家。"))
        self.memory = ConversationBufferMemory(return_messages=True)
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("你是一个花卉行家。你通常的回答不超过30字。"),
            MessagesPlaceholder(variable_name=f'{self.memory.memory_key}'),
            HumanMessagePromptTemplate.from_template("{question}"),
        ])
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True,
            memory=self.memory,
        )

    def chat_loop(self):
        print("Chatbot 已启动! 输入'exit'来退出程序。")
        while True:
            user_input = input('你: ')
            if user_input.lower() == 'exit':
                print('再见')
                break
            self.messages.append(HumanMessage(content=user_input))
            # response = self.chat(self.messages)
            response = self.conversation({"question": user_input, })
            # self.messages.append(response)
            print(f'ChatBot: {response["text"]}')


class ChatbotWithRetrieval:

    def __init__(self, doc_dir: str) -> None:
        super().__init__()
        base_dir = doc_dir
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

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        all_splits = text_splitter.split_documents(documents)

        self.vectorstore = Qdrant.from_documents(
            documents=all_splits,
            embedding=OpenAIEmbeddings(),
            location=":memory:",
            collection_name="my_documents",
        )
        self.llm = ChatOpenAI(verbose=True, model_name='gpt-4-1106-preview', )
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
        )

        retriever = self.vectorstore.as_retriever()
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
        )

    def chat_loop(self):
        print("Chatbot 已启动! 输入'exit'来退出程序。")
        while True:
            user_input = input('你: ')
            if user_input.lower() == 'exit':
                print('再见')
                break
            # self.messages.append(HumanMessage(content=user_input))
            # response = self.chat(self.messages)
            response = self.qa(user_input)
            # self.messages.append(response)
            print(f'ChatBot: {response["answer"]}')


if __name__ == '__main__':
    folder = "OneFlower"
    bot = ChatbotWithRetrieval(folder)
    bot.chat_loop()
