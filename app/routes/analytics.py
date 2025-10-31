from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.workout import WorkoutPlan
from typing import List
import statistics

router = APIRouter(prefix="/analytics", tags=["analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary/{user_id}")
def analytics_summary(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plans: List[WorkoutPlan] = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).all()
    if not plans:
        return {"message": "No plans yet for this user"}

    bmis = []
    calories = []
    for p in plans:
        pj = p.plan_json or {}
        if "bmi" in pj:
            bmis.append(float(pj["bmi"]))
        if "calories" in pj:
            calories.append(float(pj["calories"]))

    avg_bmi = round(statistics.mean(bmis), 2) if bmis else None
    avg_cal = round(statistics.mean(calories), 0) if calories else None
    last_bmi = bmis[-1] if bmis else 0
    first_bmi = bmis[0] if bmis else 0
    change = round(last_bmi - first_bmi, 2)

    insight = "Great progress!" if change < -0.5 else ("Slight improvement." if change < 0 else "Maintain consistency.")
    return {
        "user": user.name,
        "total_plans": len(plans),
        "average_bmi": avg_bmi,
        "average_calories": avg_cal,
        "bmi_change": change,
        "insight": insight
    }

@router.get("/trend/{user_id}")
def analytics_trend(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plans = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.id.asc()).all()
    trend = []
    for p in plans:
        pj = p.plan_json or {}
        trend.append({
            "plan_id": p.id,
            "created_at": str(p.created_at),
            "bmi": pj.get("bmi"),
            "calories": pj.get("calories"),
        })
    return {"user": user.name, "trend": trend}
