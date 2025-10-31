from datetime import datetime, timedelta
from random import choice, randint
from app.models.health_profile import HealthProfile
from app.models.workout_plan import WorkoutPlan
from app.core.database import SessionLocal

def generate_workout(user_id: int):
    """AI-style workout planner based on user profile"""
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    goal = user.goal.lower()
    lifestyle = user.lifestyle.lower()
    weight = user.weight
    plans = []

    categories = {
        "weight_loss": ["HIIT", "Cardio", "Core", "Yoga"],
        "muscle_gain": ["Strength", "Upper Body", "Leg Day", "Core"],
        "maintain": ["Balanced Routine", "Pilates", "Walk", "Stretch"]
    }

    intensities = ["low", "medium", "high"]

    today = datetime.now().date()

    for i in range(7):  # 7-day plan
        category = choice(categories.get(goal, ["Balanced"]))
        intensity = choice(intensities)

        # Duration (depends on lifestyle)
        duration = randint(20, 45) if lifestyle == "sedentary" else randint(30, 60)
        cal_burn = round(weight * (duration * 0.08), 1)  # rough estimate

        workout = WorkoutPlan(
            user_id=user.id,
            day=today + timedelta(days=i),
            category=category,
            workout_name=f"{category} Session {i+1}",
            duration_min=duration,
            calories_burn=cal_burn,
            intensity=intensity
        )
        db.add(workout)
        plans.append(workout)

    db.commit()
    db.close()

    return {"message": "7-day workout plan generated successfully", "user_id": user_id}
