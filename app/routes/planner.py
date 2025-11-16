from fastapi import APIRouter()
from app.services.content_planner import generate_weekly_plan
from app.models.content_plan import ContentPlan
from app.schemas.content_plan import PlanOut
from app.core.database import SessionLocal

router = APIRouter(prefix="/planner", tags=["Content Planner"])

@router.post("/generate")
def create_plan():
    """Generate 7-day AI posting plan."""
    return generate_weekly_plan()

@router.get("/all", response_model=list[PlanOut])
def get_all_plans():
    db = SessionLocal()
    plans = db.query(ContentPlan).order_by(ContentPlan.day.asc()).all()
    db.close()
    return plans
