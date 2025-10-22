import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
PDF_PATH = os.getenv("PDF_PATH", "./data/pdfs")
