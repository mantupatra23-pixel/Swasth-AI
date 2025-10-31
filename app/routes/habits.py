from fastapi import APIRouter
from app.services.ai_habit_service import generate_ai_habits, get_today_habits, update_habit_status
from app.schemas.ai_habit import HabitUpdate

router = APIRouter(prefix="/habits", tags=["AI Habit Builder"])

@router.post("/generate/{user_id}")
def create_ai_habits(user_id: int):
    """Generate AI habits for user"""
    return generate_ai_habits(user_id)

@router.get("/today/{user_id}")
def today_habits(user_id: int):
    """Get today's habits"""
    return get_today_habits(user_id)

@router.post("/update")
def update_habit(data: HabitUpdate):
    """Update habit status"""
    return update_habit_status(data.habit_id, data.completed)
