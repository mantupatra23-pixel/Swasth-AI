from app.models.reminder import Reminder
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal
from datetime import datetime, time
import smtplib, os
from email.mime.text import MIMEText

def add_reminder(data):
    db = SessionLocal()
    reminder = Reminder(
        user_id=data.user_id,
        type=data.type,
        time=data.time,
        message=data.message
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    db.close()
    return {"message": "Reminder added successfully", "id": reminder.id}


def get_all_reminders(user_id: int):
    db = SessionLocal()
    reminders = db.query(Reminder).filter(Reminder.user_id == user_id).all()
    db.close()
    return reminders


def run_reminders():
    """Trigger reminders at current system time"""
    db = SessionLocal()
    now = datetime.now().time().replace(second=0, microsecond=0)
    reminders = db.query(Reminder).filter(Reminder.active == True).all()

    triggered = []
    for r in reminders:
        if r.time.hour == now.hour and r.time.minute == now.minute:
            triggered.append(r)
            print(f"🔔 Reminder for user {r.user_id}: {r.message}")
            send_email_notification(r.user_id, r.message)

    db.close()
    return {"triggered": len(triggered), "time": now.strftime("%H:%M")}


def send_email_notification(user_id: int, message: str):
    """Optional email notification"""
    user_email = os.getenv("DEFAULT_EMAIL")  # can use Firebase token later
    if not user_email:
        return

    try:
        msg = MIMEText(message)
        msg["Subject"] = "Swasth.AI Reminder"
        msg["From"] = os.getenv("EMAIL_FROM", "no-reply@swasth.ai")
        msg["To"] = user_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        print("✅ Email reminder sent successfully")
    except Exception as e:
        print("⚠️ Email notification failed:", e)
