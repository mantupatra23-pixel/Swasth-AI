from fastapi import APIRouter()
from app.services.diet_generator import generate_diet
from app.core.database import SessionLocal
from app.models.diet_plan import DietPlan
from app.schemas.diet_plan import DietPlanOut

router = APIRouter(prefix="/diet", tags=["Diet Planner"])

@router.post("/generate/{user_id}")
def create_diet(user_id: int):
    """Generate AI diet plan for a user"""
    return generate_diet(user_id)

@router.get("/all/{user_id}", response_model=list[DietPlanOut])
def get_diet(user_id: int):
    """Fetch all diet plans for a user"""
    db = SessionLocal()
    data = db.query(DietPlan).filter(DietPlan.user_id == user_id).order_by(DietPlan.day.asc()).all()
    db.close()
    return data
