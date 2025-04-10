from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface.llms.huggingface_endpoint import HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
import os


class ChatBot():

    def __init__(self):
        load_dotenv()
        path_to_folder = "./"
        pdf_files = [f for f in os.listdir(path_to_folder) if f.endswith(".pdf")]
        documents = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(path_to_folder, pdf_file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

        recur_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=60,
            separators=["\n\n", "\n", "(?<=\. )", " ", ""],
            is_separator_regex=True,
        )

        data_splits = recur_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings()
        self.vectordb = FAISS.from_documents(data_splits, embeddings)
        self.retriever = self.vectordb.as_retriever()
        repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            temperature=0.8,
            top_p=0.8,
            top_k=50,
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_TOKEN"),
            task="text-generation"
        )
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')

        template = """
                You are a customer care chatbot. You must answer user questions based on the context provided below.
                If the answer cannot be found in the context, respond with "I don't know."
                Keep your responses concise, no longer than three sentences.

                Original Question: {question}
                Context: {context}
                Answer:
            """

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        self.conversation_chain = ConversationalRetrievalChain.from_llm(llm=self.llm,
                                                                        retriever=self.retriever,
                                                                        memory=memory,
                                                                        return_source_documents=True)

    def ask(self, input):
        response = self.conversation_chain({"question": input})
        return response['answer']
