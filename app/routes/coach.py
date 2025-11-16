from fastapi import APIRouter()
from app.services.ai_coach import chat_with_coach
from app.schemas.chat_log import ChatRequest

router = APIRouter(prefix="/coach", tags=["AI Coach"])

@router.post("/chat/{user_id}")
def chat(user_id: int, data: ChatRequest):
    """Chat with AI health coach"""
    return chat_with_coach(user_id, data.message)
