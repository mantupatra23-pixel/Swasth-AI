import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from base64 import b64encode
from openai import OpenAI
from app.models.progress_log import ProgressLog
from app.models.fitness_sync import FitnessSync
from app.models.wellness_journal import WellnessJournal
from app.core.database import SessionLocal

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_visual_report(user_id: int):
    db = SessionLocal()
    today = datetime.now()
    last_30 = today - timedelta(days=30)

    progress = db.query(ProgressLog).filter(ProgressLog.user_id == user_id, ProgressLog.created_at >= last_30).all()
    fitness = db.query(FitnessSync).filter(FitnessSync.user_id == user_id, FitnessSync.synced_at >= last_30).all()
    mood = db.query(WellnessJournal).filter(WellnessJournal.user_id == user_id).order_by(WellnessJournal.entry_date.desc()).limit(7).all()

    if not progress and not fitness:
        db.close()
        return {"message": "No progress data found."}

    # Prepare DataFrames
    progress_data = [{"date": p.created_at.date(), "bmi": p.bmi, "weight": p.weight} for p in progress]
    fit_data = [{"date": f.synced_at.date(), "steps": f.steps, "calories": f.calories_burned, "sleep": f.sleep_hours} for f in fitness]

    df1 = pd.DataFrame(progress_data)
    df2 = pd.DataFrame(fit_data)

    # Merge & fill missing
    df = pd.merge(df1, df2, on="date", how="outer").fillna(method="ffill")

    # Create chart
    plt.figure(figsize=(10,6))
    plt.plot(df["date"], df["steps"], label="Steps", linewidth=2)
    plt.plot(df["date"], df["calories"], label="Calories Burned", linewidth=2)
    plt.plot(df["date"], df["bmi"], label="BMI", linewidth=2)
    plt.legend()
    plt.title("Your 30-Day Health Progress (Swasth.AI)")
    plt.xlabel("Date")
    plt.ylabel("Metrics")
    plt.grid(True)
    plt.tight_layout()

    # Convert to base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encoded = b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # AI summary
    mood_summary = " ".join([m.mood for m in mood]) if mood else "neutral"
    prompt = f"""
    User’s recent trend: {len(df)} days of data.
    Average steps: {df['steps'].mean() if 'steps' in df else 0:.0f}.
    Average calories: {df['calories'].mean() if 'calories' in df else 0:.0f}.
    BMI trend last 30 days: {df['bmi'].iloc[-1] if 'bmi' in df else 'N/A'}.
    Mood pattern: {mood_summary}.
    Write a short encouraging summary of their overall wellness improvement.
    """

    try:
        ai_summary = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI fitness coach giving emotional and data-driven feedback."},
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message.content.strip()
    except Exception:
        ai_summary = "Your consistency is impressive! Keep moving, stay mindful, and trust your growth 💪🌿."

    db.close()
    return {
        "chart": f"data:image/png;base64,{encoded}",
        "summary": ai_summary
    }
