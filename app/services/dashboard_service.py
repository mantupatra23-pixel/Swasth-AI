from app.models.health_profile import HealthProfile
from app.models.progress_log import ProgressLog
from app.models.health_log import HealthLog
from app.models.workout_plan import WorkoutPlan
from app.models.diet_plan import DietPlan
from app.core.database import SessionLocal
from datetime import datetime, timedelta

def get_dashboard(user_id: int):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        db.close()
        return {"error": "User not found"}

    # Fetch last 30 days data
    last_30 = datetime.now() - timedelta(days=30)
    progress = db.query(ProgressLog).filter(ProgressLog.user_id == user_id, ProgressLog.created_at >= last_30).all()
    health = db.query(HealthLog).filter(HealthLog.user_id == user_id, HealthLog.created_at >= last_30).all()

    # Basic summaries
    avg_bmi = round(sum([p.bmi for p in progress]) / len(progress), 2) if progress else user.bmi
    avg_risk = round(sum([h.risk_score for h in health]) / len(health), 2) if health else 80

    # Streak logic
    streak = len(progress)
    level = "Gold 🥇" if streak >= 20 else "Silver 🥈" if streak >= 10 else "Bronze 🥉"

    # AI insight generation
    if avg_risk > 85:
        insight = "Excellent balance of diet and activity! Keep maintaining your routine. 💪"
    elif avg_risk > 60:
        insight = "Good job! Try to improve your sleep schedule for better energy."
    else:
        insight = "You might be under stress. Revisit your diet and rest days."

    db.close()

    return {
        "user_id": user.id,
        "name": user.name,
        "goal": user.goal,
        "premium_status": user.is_premium,
        "avg_bmi": avg_bmi,
        "avg_health_score": avg_risk,
        "streak_days": streak,
        "level": level,
        "ai_insight": insight,
        "message": "Dashboard summary generated successfully."
    }
