from fastapi import APIRouter
from pydantic import BaseModel
# from ..services.openai_service import get_chatbot

from ..services.openai_service import get_chatbot_anthropic
qa_chain = get_chatbot_anthropic()

router = APIRouter()
# qa_chain = get_chatbot()

class Question(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(payload: Question):
    try:
        answer = qa_chain.invoke(payload.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
