from pydantic import BaseModel
from datetime import datetime

class HealthLogCreate(BaseModel):
    user_id: int
    systolic_bp: float
    diastolic_bp: float
    sugar_level: float
    heart_rate: float
    sleep_hours: float

class HealthLogOut(BaseModel):
    id: int
    user_id: int
    systolic_bp: float
    diastolic_bp: float
    sugar_level: float
    heart_rate: float
    sleep_hours: float
    risk_score: float
    created_at: datetime

    class Config:
        orm_mode = True
