from pydantic import BaseModel
from typing import Any

class PlanOut(BaseModel):
    calories: int
    bmi: float
    workouts: Any
    message: str
