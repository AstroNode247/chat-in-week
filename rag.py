# Document loading
from abc import ABC, abstractmethod

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Milvus

from model import ChatGemini, BaseLLM


class FileLoader(ABC):
    def __init__(self):
        self.collection_name = None
        self.docs = None

    @abstractmethod
    def load_file(self, path: str) -> str:
        pass

    def split_document(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        self.docs = text_splitter.split_documents(self.docs)

    def load_embeddings(self, llm: BaseLLM, collection_name: str, path: str = None):
        connection_args = {"host": "127.0.0.1", "port": "19530"}
        self.collection_name = collection_name
        if path is None:
            self.collection_name = collection_name
            db = Milvus(llm.embedding, connection_args=connection_args,
                        collection_name=self.collection_name)
        else:
            self.load_file(path=path)
            self.split_document()
            db = Milvus.from_documents(self.docs, llm.embedding, connection_args=connection_args,
                                       collection_name=self.collection_name)

        return db


class PDFLoader(FileLoader):
    def __init__(self):
        super().__init__()

    def load_file(self, path: str):
        loader = PyPDFLoader(path)
        self.docs = loader.load()


class CSVParser(FileLoader):
    def __init__(self):
        super().__init__()

    def load_file(self, path: str):
        loader = CSVLoader(path)
        self.docs = loader.load()


if __name__ == "__main__":
    # Load the documents
    print("Prepraring data")
    chat_model = ChatGemini()
    db = CSVParser().load_embeddings(path="data\events_clean.csv",
                                collection_name="ecommerce_events", llm=chat_model)

    query = "What are the phones disponible ?"
    docs = db.similarity_search(query)

    print(docs[:3])

# Model loading

# Chain creation
