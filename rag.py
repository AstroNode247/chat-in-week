# Document loading
from pypdf import PdfReader
from langchain_community.vectorstores import Milvus
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader

from model import get_embedding_model

# Load PDF document
def get_pdf_document(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def load_pdf_document(pdf_docs):
    loader = PyPDFLoader(pdf_docs)
    docs = loader.load()
    return docs


def load_csv_document(csv_doc):
    loader = CSVLoader(csv_doc)
    docs = loader.load()
    return docs

# Document splitting
def split_document(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs_splitted = text_splitter.split_documents(docs)

    return docs_splitted


# Vectorization
def load_vectorized_docs(collection_name, docs=None):
    # Load Weaviate client 
    embeddings = get_embedding_model()
    connection_args={"host": "127.0.0.1", "port": "19530"}
    if docs is None:
       db = Milvus(embeddings, connection_args=connection_args,
                                collection_name=collection_name) 
    else:
        db = Milvus.from_documents(docs, embeddings, connection_args=connection_args,
                                    collection_name=collection_name)

    return db


if __name__ == "__main__":
    # Load the documents
    print("Prepraring data")
    docs = load_csv_document("data\events_clean.csv")
    docs = split_document(docs)

    print("Load to Milvus")
    db = load_vectorized_docs("Event_Ecom", docs)

    query = "I want to find a gift for my sister. What is the best phone ?"
    docs = load_vectorized_docs(docs).similarity_search(query)

    print(docs[:3])


    

# Model loading

# Chain creation


