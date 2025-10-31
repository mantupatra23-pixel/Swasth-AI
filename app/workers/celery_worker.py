from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.user import User
from app.models.workout import WorkoutPlan
from app.services.ai_engine import generate_plan_from_profile
import datetime
from app.services.notifier import send_email_notification, send_telegram_notification

# Celery Config
celery = Celery(
    "swasthai_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="generate_weekly_plans")
def generate_weekly_plans():
    db = SessionLocal()
    users = db.query(User).all()
    count = 0
    for user in users:
        plan = generate_plan_from_profile({
            "weight": user.weight,
            "height": user.height,
            "goal": user.goal
        })
        wp = WorkoutPlan(
            user_id=user.id,
            name=f"Weekly Plan {datetime.date.today()}",
            source="auto_celery",
            plan_json=plan
        )
        db.add(wp)
        count += 1
    db.commit()
    db.close()
    return f"Generated {count} weekly plans successfully ✅"

# --- send notifications ---
for user in users:
    subject = "🩺 Swasth.AI — Your new AI Health Plan is ready!"
    body = f"Hello {user.name},\n\nYour new AI-based fitness plan has been generated.\nLog in to the app to view it.\n\nStay healthy!\nTeam Swasth.AI"
    send_email_notification(user.name + "@example.com", subject, body)
    send_telegram_notification(f"New plan generated for {user.name} ✅")
