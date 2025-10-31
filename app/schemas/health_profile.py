from pydantic import BaseModel
from datetime import datetime

class HealthProfileCreate(BaseModel):
    name: str
    age: int
    gender: str
    height: float
    weight: float
    goal: str
    lifestyle: str

class HealthProfileOut(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    height: float
    weight: float
    goal: str
    lifestyle: str
    bmi: float
    bmr: float
    ideal_weight: float
    calories_required: float
    created_at: datetime

    class Config:
        orm_mode = True
