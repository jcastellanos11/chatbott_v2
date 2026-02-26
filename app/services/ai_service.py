import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from ..utils.config import PDF_PATH, VECTOR_DB_PATH, ANTHROPIC_API_KEY

from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import HuggingFaceEmbeddings  # Agrega esta importación


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
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if not os.path.exists(VECTOR_DB_PATH) or len(os.listdir(VECTOR_DB_PATH)) == 0:
        raise RuntimeError(
            f"No existe la base vectorial en {VECTOR_DB_PATH}. "
            "Primero ejecuta rebuild_vector_db.py para construirla (PDF + código)."
        )

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name="orfeo_unificado"
    )

    return vectorstore




def get_chatbot_anthropic():
    """
    Construye el chatbot usando Anthropic Claude.
    Ideal para leer PDFs extensos con estructuras complejas.
    """
    vectorstore = get_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})



    llm = ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0,
        api_key=ANTHROPIC_API_KEY
    )

    prompt = ChatPromptTemplate.from_template(
        """
            Eres un asistente experto en el sistema Orfeo–SGDEA.
            “Orfeo” es el nombre del software de gestión documental y de expedientes (SGDEA),
            no una referencia artística, musical o mitológica.

            Tu objetivo es ayudar de forma clara, técnica y amigable 😊,
            explicando el funcionamiento del sistema Orfeo–SGDEA a partir del CONTEXTO proporcionado,
            el cual puede incluir fragmentos de código fuente, documentación técnica (PDF)
            y textos explicativos.

            🧠 Reglas de conocimiento:
            - Usa ÚNICAMENTE la información presente en el CONTEXTO.
            - No inventes información ni supongas comportamientos que no estén respaldados
            explícita o implícitamente por el contexto.
            - Si el contexto incluye código, analízalo y explica:
            ▸ su propósito
            ▸ el flujo lógico general
            ▸ cómo se relaciona con Orfeo–SGDEA
            - Si el contexto incluye tablas, listados o estructuras, reprodúcelos de forma clara.

            🗣️ Estilo de respuesta:
            - Responde siempre en español técnico, claro y preciso.
            - Utiliza iconos (por ejemplo: 🔹 📌 ⚠️ ✅ ❓) para organizar la explicación.
            - Usa listas y secciones cuando ayuden a la comprensión.
            - Mantén un tono profesional pero cercano y pedagógico.

            ⚠️ Si el contexto es parcial o insuficiente:
            - Indica claramente qué información falta.
            - Explica por qué esa información es necesaria.
            - Sugiere qué tipo de documento ayudaría a responder mejor
            (manual funcional, documentación del módulo, comentarios en el código, etc.).

            CONTEXTO:
            {context}

            PREGUNTA:
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
