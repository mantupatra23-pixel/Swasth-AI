import os
from datetime import date
from openai import OpenAI
from app.models.wellness_journal import WellnessJournal
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def add_journal_entry(user_id: int, mood: str, content: str):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    prompt = f"""
    The user wrote the following journal entry:
    "{content}"
    Their mood is: {mood}.
    Generate a short, kind, AI wellness coach response to comfort and motivate them.
    """

    try:
        ai_reply = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic wellness coach focused on emotional healing."},
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message.content.strip()
    except Exception:
        ai_reply = "You’re doing well. Take small steps, breathe deeply, and trust the process 🌱."

    entry = WellnessJournal(
        user_id=user_id,
        mood=mood,
        content=content,
        ai_feedback=ai_reply
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    db.close()

    return {
        "message": "Journal entry added successfully",
        "ai_feedback": ai_reply
    }


def get_today_entry(user_id: int):
    db = SessionLocal()
    entry = db.query(WellnessJournal).filter(
        WellnessJournal.user_id == user_id,
        WellnessJournal.entry_date == date.today()
    ).first()
    db.close()
    if not entry:
        return {"message": "No journal entry found for today."}
    return {
        "mood": entry.mood,
        "content": entry.content,
        "ai_feedback": entry.ai_feedback,
        "entry_date": entry.entry_date
    }


def get_ai_insight(user_id: int):
    db = SessionLocal()
    entries = db.query(WellnessJournal).filter(WellnessJournal.user_id == user_id).order_by(WellnessJournal.entry_date.desc()).limit(7).all()
    if not entries:
        db.close()
        return {"message": "No entries available for insight."}

    all_text = " ".join([f"{e.mood}: {e.content}" for e in entries])

    prompt = f"""
    Based on these 7 days of emotional reflections:
    {all_text}
    Summarize the user's emotional pattern and give positive advice for their upcoming week.
    """

    try:
        ai_summary = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a mental wellness assistant summarizing emotions positively."},
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message.content.strip()
    except Exception:
        ai_summary = "Overall, you’re progressing toward emotional balance. Keep focusing on gratitude and self-care 💖."

    db.close()
    return {"weekly_insight": ai_summary}
