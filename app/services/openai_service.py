import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from ..utils.config import OPENAI_API_KEY, PDF_PATH, VECTOR_DB_PATH


def load_documents():
    """
    Carga uno o varios PDFs usando UnstructuredPDFLoader.
    Extrae texto y realiza OCR si hay imágenes con texto.
    """
    docs = []
    if os.path.isdir(PDF_PATH):
        for filename in os.listdir(PDF_PATH):
            if filename.endswith(".pdf"):
                loader = UnstructuredPDFLoader(
                    os.path.join(PDF_PATH, filename),
                    strategy="hi_res",        # usa OCR de alta calidad
                    languages=["spa"]
                )
                docs.extend(loader.load())
    else:
        loader = UnstructuredPDFLoader(PDF_PATH)
        docs.extend(loader.load())
    return docs


def split_docs(docs):
    """
    Divide los documentos largos en fragmentos manejables.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(docs)


def get_vector_store():
    """
    Crea o carga la base vectorial persistente (ChromaDB)
    usando embeddings de OpenAI.
    """
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)


    print(" get_vector_store...")

    if not os.path.exists(VECTOR_DB_PATH) or len(os.listdir(VECTOR_DB_PATH)) == 0:
        print("🔄 Creando nueva base vectorial desde PDFs...")
        docs = load_documents()
        split_chunks = split_docs(docs)
        vectorstore = Chroma.from_documents(
            split_chunks, embedding=embeddings, persist_directory=VECTOR_DB_PATH
        )
        vectorstore.persist()
        print("✅ Base vectorial creada y guardada.")

        print(f"📄 Documentos cargados: {len(docs)}")
        print(f"✂️ Fragmentos creados: {len(split_chunks)}")
    else:
        print("📦 Cargando base vectorial existente...")
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH, embedding_function=embeddings
        )
    
   


    return vectorstore


def get_chatbot():
    """
    Construye la cadena moderna de LangChain para preguntas y respuestas.
    """
    vectorstore = get_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

    prompt = ChatPromptTemplate.from_template(
        """Eres un asistente experto en el sistema Orfeo-SGDEA.
        Tu objetivo es responder *exclusivamente* usando la información del contexto siguiente,
        que proviene directamente del manual de usuario del SGDEA.

        - Si el contexto contiene una tabla, formato o estructura específica, reprodúcela de forma clara.
        - No generalices ni inventes datos.
        - Si el contexto no tiene información suficiente, responde: "No tengo información suficiente para responder."
        - Siempre responde en español técnico y claro.
        - Responde siempre usando formato Markdown cuando el contexto tenga listas o estructuras.

        Contexto:
        {context}

        Pregunta:
        {question}

        
        """
    )


    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
