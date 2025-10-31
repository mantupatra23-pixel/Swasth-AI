from pydantic import BaseModel
from datetime import date

class JournalEntry(BaseModel):
    user_id: int
    mood: str
    content: str

class JournalOut(BaseModel):
    id: int
    mood: str
    content: str
    ai_feedback: str
    entry_date: date

    class Config:
        orm_mode = True
