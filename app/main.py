from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat

app = FastAPI(title="Orfeo Chatbot API", version="1.0")

# CORS - para desarrollo puedes usar ["*"], en producción restringe a tus orígenes.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    # "https://tu-dominio.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o usar `origins` en lugar de ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "API del Chatbot de Orfeo funcionando 🚀"}
