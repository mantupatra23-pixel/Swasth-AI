import json
import os
from datetime import datetime
from openai import OpenAI
from app.models.health_profile import HealthProfile
from app.models.health_log import HealthLog
from app.models.progress_log import ProgressLog
from app.models.wellness_journal import WellnessJournal
from app.models.fitness_sync import FitnessSync
from app.models.ai_habit import AIHabit
from app.core.database import SessionLocal
from app.core.supabase_client import supabase

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def backup_user_data(user_id: int):
    """AI-based compression + cloud sync backup"""
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    logs = db.query(HealthLog).filter(HealthLog.user_id == user_id).all()
    progress = db.query(ProgressLog).filter(ProgressLog.user_id == user_id).all()
    journal = db.query(WellnessJournal).filter(WellnessJournal.user_id == user_id).all()
    fitness = db.query(FitnessSync).filter(FitnessSync.user_id == user_id).all()
    habits = db.query(AIHabit).filter(AIHabit.user_id == user_id).all()

    combined_data = {
        "user": {"id": user.id, "name": user.name, "goal": user.goal},
        "logs": [l.__dict__ for l in logs],
        "progress": [p.__dict__ for p in progress],
        "journal": [j.__dict__ for j in journal],
        "fitness": [f.__dict__ for f in fitness],
        "habits": [h.__dict__ for h in habits]
    }

    # Compress summary using GPT
    try:
        res = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You compress JSON health data into a short readable insight summary."},
                {"role": "user", "content": json.dumps(combined_data)[:10000]}
            ]
        )
        summary = res.choices[0].message.content.strip()
    except Exception:
        summary = "Health data compressed summary could not be generated."

    # Upload JSON to Supabase
    filename = f"backup_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump({"summary": summary, "data": combined_data}, f, indent=2)

    supabase.storage.from_("swasthai_backups").upload(filename, filename)
    os.remove(filename)
    db.close()

    return {"message": "Backup successful", "backup_file": filename}


def restore_user_data(user_id: int, filename: str):
    """Restore last backup from Supabase"""
    try:
        file = supabase.storage.from_("swasthai_backups").download(filename)
        content = json.loads(file)
        return {"message": "Backup restored successfully", "data": content}
    except Exception as e:
        return {"error": f"Failed to restore backup: {e}"}
