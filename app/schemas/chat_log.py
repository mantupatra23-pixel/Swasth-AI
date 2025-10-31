from pydantic import BaseModel
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str
    created_at: datetime
