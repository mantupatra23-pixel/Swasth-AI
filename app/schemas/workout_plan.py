from pydantic import BaseModel
from datetime import date, datetime

class WorkoutPlanOut(BaseModel):
    id: int
    user_id: int
    day: date
    category: str
    workout_name: str
    duration_min: int
    calories_burn: float
    intensity: str
    created_at: datetime

    class Config:
        orm_mode = True
