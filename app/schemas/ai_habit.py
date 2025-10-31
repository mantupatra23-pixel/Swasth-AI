from pydantic import BaseModel
from datetime import date

class HabitCreate(BaseModel):
    user_id: int
    title: str
    description: str
    frequency: str

class HabitUpdate(BaseModel):
    habit_id: int
    completed: bool

class HabitOut(BaseModel):
    id: int
    title: str
    description: str
    frequency: str
    created_at: date
    class Config:
        orm_mode = True
