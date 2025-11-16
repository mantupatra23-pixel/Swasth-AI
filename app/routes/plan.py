from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.workout import WorkoutPlan
from app.services.ai_engine import generate_plan_from_profile
from app.schemas.user import UserCreate
from app.schemas.plan import PlanOut

router = APIRouter()

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


@router.get("/plan/generate-from-user/{user_id}")
def generate_plan_from_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch last workout plan
    last = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.id.desc())
        .first()
    )

    last_weight = user.weight
    if last:
        try:
            old_weight = float(last.plan_json.get("bmi", 0)) * ((user.height / 100) ** 2)
            last_weight = old_weight
        except Exception:
            pass

    plan = generate_plan_from_profile(
        {
            "weight": user.weight,
            "height": user.height,
            "goal": user.goal,
        }
    )

    wp = WorkoutPlan(
        user_id=user.id,
        name="AI Plan",
        source="ai_engine",
        plan_json=plan,
    )
    db.add(wp)
    db.commit()
    db.refresh(wp)

    return {"plan_id": wp.id, "plan": plan}


@router.post("/plan/auto-refresh")
def trigger_auto_refresh():
    from app.workers.celery_worker import generate_weekly_plans
    job = generate_weekly_plans.delay()
    return {"status": "Started background weekly plan generation", "job_id": job.id}
