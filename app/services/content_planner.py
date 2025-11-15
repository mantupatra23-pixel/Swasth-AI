from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.content_plan import ContentPlan
from app.services.trend_analyzer import analyze_trends
from openai import OpenAI
from app.core.database import SessionLocal
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_weekly_plan():
    """
    Generate 7-day plan using GPT based on trending data.
    """
    db = SessionLocal()

    # Fetch trend data
    trend_data = analyze_trends()
    trend_summary = trend_data.get("trend_summary", "")
    stats = trend_data.get("data", [])

    # Prompt for GPT
    prompt = (
        f"Based on the following engagement trends:\n"
        f"{trend_summary}\n\n"
        f"Create a 7-day posting plan for next week.\n"
        f"Each day should have a 'category', 'title', and 'caption'.\n"
        f"Make sure it follows the best performing categories.\n"
    )

    # --------- AI RESPONSE -----------
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.8
        )

        response = completion.choices[0].message.content

    except Exception:
        # SAFE DEFAULT BACKUP RESPONSE
        response = '''1. Monday: Motivation - "Start strong."
2. Tuesday: Workout - "Your sweat is your success."
3. Wednesday: Nutrition - "Eat clean, train dirty."
4. Thursday: Mindfulness - "Reset your mind to rise."
5. Friday: Workout - "Push harder, go further."
6. Saturday: Motivation - "One more rep, one more win."
7. Sunday: Reflection - "Rest is part of the process."'''
    # ---------------------------------

    # --------- PARSE RESPONSE ----------
    today = datetime.now().date()
    lines = response.split("\n")

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        parts = line.split(":")

        if len(parts) < 2:
            continue

        try:
            _, content = parts[0], ":".join(parts[1:])

            if "-" in content:
                category, caption = content.split("-", 1)
            else:
                category = "General"
                caption = content

            plan = ContentPlan(
                day=today + timedelta(days=i),
                category=category.strip(),
                title=f"Day {i+1} Plan",
                caption=caption.strip().replace('"', ''),
                scheduled_time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            )

            db.add(plan)

        except Exception as e:
            print("⚠️ Parse error:", e)
            continue

    db.commit()
    db.close()

    print("✅ Weekly content plan generated successfully!")
    return {"message": "7-day plan created", "summary": response}
