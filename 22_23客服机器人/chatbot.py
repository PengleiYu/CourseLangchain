# 聊天机器人，支持streamlet、gradio部署
import os
import streamlit as st
import gradio as gr
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
        print(f"开始读取文件夹:{os.path.abspath(base_dir)}")
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
        print("开始分割文档")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        all_splits = text_splitter.split_documents(documents)

        print("开始创建矢量DB")
        self.vectorstore = Qdrant.from_documents(
            documents=all_splits,
            embedding=OpenAIEmbeddings(),
            location=":memory:",
            collection_name="my_documents",
        )
        print("开始创建llm")
        self.llm = ChatOpenAI(verbose=True, model_name='gpt-4-1106-preview', )
        print("开始创建memory")
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
        )
        print("开始创建检索对象")
        retriever = self.vectorstore.as_retriever()
        print("开始创建会话检索链")
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
        )

        self.conversation_history = ""
        print("初始化完成")

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

    def get_response(self, user_input: str):
        response = self.qa(user_input)
        self.conversation_history += f"你:{user_input}\nChatbot:{response['answer']}\n"
        return self.conversation_history


def main_stream_let():
    st.title('易速鲜花聊天客服')
    if 'bot' not in st.session_state:
        folder = "22_23客服机器人/OneFlower"
        st.session_state.bot = ChatbotWithRetrieval(folder)
    user_input = st.text_input('请输入你的问题')
    if user_input:
        response = st.session_state.bot.qa(user_input)
        st.write(f'Chatbot: {response["answer"]}')


def main_gradio():
    folder = "22_23客服机器人/OneFlower"
    bot = ChatbotWithRetrieval(folder)
    interface = gr.Interface(
        fn=bot.get_response,
        inputs='text',
        outputs='text',
        live=False,
        title='易速鲜花聊天客服',
        description='请输入问题，然后点击提交',
    )
    interface.launch()


if __name__ == '__main__':
    # main_stream_let()
    main_gradio()
