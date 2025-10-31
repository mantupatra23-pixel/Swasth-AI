from datetime import datetime
from app.models.ai_habit import AIHabit
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal

def send_daily_reminders():
    """Send daily reminders for habits and workouts"""
    db = SessionLocal()
    users = db.query(HealthProfile).all()

    now = datetime.now().strftime("%H:%M")
    for user in users:
        habits = db.query(AIHabit).filter(AIHabit.user_id == user.id, AIHabit.active == True).all()
        for h in habits:
            print(f"🔔 Reminder for {user.name}: Complete your habit - {h.title}")

    db.close()
    return {"message": f"Reminders sent at {now}"}
