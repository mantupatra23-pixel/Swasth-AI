from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.workout import WorkoutPlan
from app.services.ai_engine import generate_plan_from_profile
from app.schemas.user import UserCreate
from app.schemas.plan import PlanOut

router = APIRouter(tags=["plan"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/plan/generate", response_model=PlanOut)
def generate_plan(payload: UserCreate):
    profile = payload.dict()
    plan = generate_plan_from_profile(profile)
    return plan
