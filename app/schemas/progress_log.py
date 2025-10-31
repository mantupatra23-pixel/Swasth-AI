from pydantic import BaseModel
from datetime import datetime

class ProgressCreate(BaseModel):
    user_id: int
    weight: float
    calories_intake: float
    calories_burned: float

class ProgressOut(BaseModel):
    id: int
    user_id: int
    weight: float
    bmi: float
    calories_intake: float
    calories_burned: float
    progress_score: float
    created_at: datetime

    class Config:
        orm_mode = True
