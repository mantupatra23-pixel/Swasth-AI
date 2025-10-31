from app.models.progress_log import ProgressLog
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal
from datetime import datetime, timedelta

def add_progress(data):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == data.user_id).first()
    if not user:
        return {"error": "User not found"}

    # Recalculate BMI
    bmi = round(data.weight / ((user.height / 100) ** 2), 2)

    # Progress score logic (AI style)
    calorie_diff = data.calories_burned - data.calories_intake
    bmi_diff = user.bmi - bmi

    score = 50
    score += (bmi_diff * 10)
    score += (calorie_diff / 100)

    score = max(0, min(100, round(score, 1)))

    progress = ProgressLog(
        user_id=data.user_id,
        weight=data.weight,
        bmi=bmi,
        calories_intake=data.calories_intake,
        calories_burned=data.calories_burned,
        progress_score=score
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)
    db.close()

    return {"message": "Progress added successfully", "progress_score": score}

def get_weekly_report(user_id: int):
    db = SessionLocal()
    last_7_days = datetime.now() - timedelta(days=7)
    logs = db.query(ProgressLog).filter(ProgressLog.user_id == user_id, ProgressLog.created_at >= last_7_days).all()

    if not logs:
        db.close()
        return {"message": "No data for this week"}

    avg_bmi = round(sum([x.bmi for x in logs]) / len(logs), 2)
    avg_score = round(sum([x.progress_score for x in logs]) / len(logs), 2)
    avg_burn = round(sum([x.calories_burned for x in logs]) / len(logs), 1)
    avg_intake = round(sum([x.calories_intake for x in logs]) / len(logs), 1)

    trend = "improving" if avg_score > 60 else "stable" if avg_score > 45 else "needs attention"

    db.close()
    return {
        "user_id": user_id,
        "average_bmi": avg_bmi,
        "average_score": avg_score,
        "avg_calories_burned": avg_burn,
        "avg_calories_intake": avg_intake,
        "trend": trend,
        "message": f"Your performance this week is {trend} (Score: {avg_score}/100)"
    }
