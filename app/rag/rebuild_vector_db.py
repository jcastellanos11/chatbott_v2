import os
import json
import shutil
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------------
# RUTAS (ajusta si aplica)
# -------------------------

PDF_PATH = "data/pdfs"  # carpeta donde guardas PDFs (o un archivo .pdf)
CODE_CHUNKS_PATH = "data/code/code_chunks.json"

# Base final consolidada (PDF + Código)
VECTOR_DB_PATH = "data/vector_db_unificado"
COLLECTION_NAME = "orfeo_unificado"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# PDFs: mismos parámetros que ya vienes usando
PDF_CHUNK_SIZE = 800
PDF_CHUNK_OVERLAP = 100


def load_pdfs(pdf_path: str) -> List[Document]:
    docs: List[Document] = []

    if os.path.isdir(pdf_path):
        for filename in os.listdir(pdf_path):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(pdf_path, filename)
                loader = UnstructuredPDFLoader(
                    full_path,
                    strategy="hi_res",
                    languages=["spa"]
                )
                loaded = loader.load()
                # marcar metadata
                for d in loaded:
                    d.metadata = d.metadata or {}
                    d.metadata.update({
                        "source": "pdf",
                        "pdf_file": filename
                    })
                docs.extend(loaded)
    else:
        # archivo individual
        loader = UnstructuredPDFLoader(pdf_path, strategy="hi_res", languages=["spa"])
        loaded = loader.load()
        for d in loaded:
            d.metadata = d.metadata or {}
            d.metadata.update({
                "source": "pdf",
                "pdf_file": os.path.basename(pdf_path)
            })
        docs.extend(loaded)

    return docs


def split_pdf_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=PDF_CHUNK_SIZE,
        chunk_overlap=PDF_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(docs)


def load_code_chunks(json_path: str) -> List[Document]:
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"No existe code_chunks.json en: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    docs: List[Document] = []
    for item in chunks:
        content = (item.get("content") or "").strip()
        if not content:
            continue

        md = item.get("metadata") or {}

        md.setdefault("file", "unknown")
        md.setdefault("path", "unknown")
        md.setdefault("module", "unknown")

        md.update({
            "source": "code",
            "chunk_id": item.get("id")
        })
        docs.append(Document(page_content=content, metadata=md))

    return docs


def rebuild_vector_db():
    print("Inicializando embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # 1) PDFs
    print(f"Cargando PDFs desde: {PDF_PATH}")
    pdf_docs = load_pdfs(PDF_PATH)
    print(f"PDF docs cargados (sin chunk): {len(pdf_docs)}")

    print("Haciendo chunking de PDFs...")
    pdf_chunks = split_pdf_docs(pdf_docs)
    print(f"PDF chunks: {len(pdf_chunks)}")

    # 2) Código (ya viene chunked desde el pipeline)
    print(f"Cargando chunks de código desde: {CODE_CHUNKS_PATH}")
    code_docs = load_code_chunks(CODE_CHUNKS_PATH)
    print(f"Code chunks: {len(code_docs)}")

    # 3) Unir
    all_docs = pdf_chunks + code_docs
    # all_docs = code_docs
    print(f"TOTAL documentos para indexar: {len(all_docs)}")

    # 4) Rebuild limpio (borrando base anterior unificada)
    if os.path.exists(VECTOR_DB_PATH):
        print(f"Borrando base anterior en: {VECTOR_DB_PATH}")
        shutil.rmtree(VECTOR_DB_PATH)

    # 5) Crear base unificada

    print("EJEMPLO DE DOCUMENTO DE CÓDIGO:")
    print(code_docs[0].page_content[:300])
    print("METADATA:")
    print(code_docs[0].metadata)

    print("Creando Chroma unificado (PDF + Código)...")
    vectorstore = Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
        collection_name=COLLECTION_NAME
    )
    vectorstore.persist()

    print("✅ Rebuild completado.")
    print(f"Ruta base unificada: {VECTOR_DB_PATH}")
    print(f"Colección: {COLLECTION_NAME}")


if __name__ == "__main__":
    rebuild_vector_db()
