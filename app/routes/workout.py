from fastapi import APIRouter()
from app.services.workout_generator import generate_workout
from app.core.database import SessionLocal
from app.models.workout_plan import WorkoutPlan
from app.schemas.workout_plan import WorkoutPlanOut

router = APIRouter(prefix="/workout", tags=["Workout Planner"])

@router.post("/generate/{user_id}")
def create_plan(user_id: int):
    """Generate 7-day AI workout plan for a user"""
    return generate_workout(user_id)

@router.get("/all/{user_id}", response_model=list[WorkoutPlanOut])
def get_workouts(user_id: int):
    """Get all workouts for a user"""
    db = SessionLocal()
    data = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.day.asc()).all()
    db.close()
    return data
