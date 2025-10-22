import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from ..utils.config import PDF_PATH, VECTOR_DB_PATH

def load_documents():
    """Carga todos los PDFs en la carpeta data/pdfs"""
    docs = []
    for filename in os.listdir(PDF_PATH):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_PATH, filename))
            docs.extend(loader.load())
    return docs

def get_vector_store():
    """Crea o carga la base vectorial Chroma"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    if not os.path.exists(VECTOR_DB_PATH) or len(os.listdir(VECTOR_DB_PATH)) == 0:
        docs = load_documents()
        vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=VECTOR_DB_PATH)
        vectorstore.persist()
    else:
        vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
    return vectorstore
