from fastapi import FastAPI
from app.routes import chat

app = FastAPI(title="Orfeo Chatbot API", version="1.0")
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "API del Chatbot de Orfeo funcionando 🚀"}
