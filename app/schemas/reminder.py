from pydantic import BaseModel
from datetime import time, datetime

class ReminderCreate(BaseModel):
    user_id: int
    type: str
    time: time
    message: str

class ReminderOut(BaseModel):
    id: int
    user_id: int
    type: str
    time: time
    message: str
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True
