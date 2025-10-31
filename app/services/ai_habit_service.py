import os
from datetime import date
from openai import OpenAI
from app.models.ai_habit import AIHabit
from app.models.habit_progress import HabitProgress
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_habits(user_id: int):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Generate habits using GPT
    prompt = f"""
    Generate 5 healthy daily habits for a person with the following profile:
    Goal: {user.goal}, Age: {user.age}, Lifestyle: {user.lifestyle}.
    Keep them short, specific, and measurable. Output format:
    Habit Title - Description.
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a health habit coach."},
                      {"role": "user", "content": prompt}]
        )
        habits_text = res.choices[0].message.content.strip()
    except Exception:
        habits_text = """
        Drink 2L water daily - Stay hydrated and improve metabolism.
        10-min meditation - Improve focus and reduce stress.
        Sleep 7+ hours - Maintain energy and recovery.
        Walk 5000 steps - Boost stamina.
        Eat fruit post-lunch - Add natural vitamins.
        """

    # Parse and save habits
    created = []
    for line in habits_text.split("\n"):
        if "-" in line:
            title, desc = line.split("-", 1)
            habit = AIHabit(user_id=user.id, title=title.strip(), description=desc.strip(), frequency="daily")
            db.add(habit)
            db.commit()
            db.refresh(habit)

            progress = HabitProgress(habit_id=habit.id, completed=False)
            db.add(progress)
            db.commit()
            created.append({"title": title.strip(), "description": desc.strip()})

    db.close()
    return {"message": "AI habits generated successfully", "habits": created}


def get_today_habits(user_id: int):
    db = SessionLocal()
    habits = db.query(AIHabit).filter(AIHabit.user_id == user_id, AIHabit.active == True).all()
    results = []
    for h in habits:
        progress = db.query(HabitProgress).filter(HabitProgress.habit_id == h.id, HabitProgress.date == date.today()).first()
        results.append({
            "id": h.id,
            "title": h.title,
            "description": h.description,
            "completed": progress.completed if progress else False
        })
    db.close()
    return results


def update_habit_status(habit_id: int, completed: bool):
    db = SessionLocal()
    progress = db.query(HabitProgress).filter(HabitProgress.habit_id == habit_id, HabitProgress.date == date.today()).first()
    if not progress:
        progress = HabitProgress(habit_id=habit_id, completed=completed)
        db.add(progress)
    else:
        progress.completed = completed
    db.commit()
    db.close()
    return {"message": f"Habit marked as {'completed' if completed else 'pending'}."}
