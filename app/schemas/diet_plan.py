from pydantic import BaseModel
from datetime import date, datetime

class DietPlanOut(BaseModel):
    id: int
    user_id: int
    day: date
    meal_type: str
    food_items: str
    calories: float
    protein: float
    carbs: float
    fats: float
    created_at: datetime

    class Config:
        orm_mode = True
