from datetime import datetime, timedelta
from random import choice, randint
from app.models.health_profile import HealthProfile
from app.models.diet_plan import DietPlan
from app.core.database import SessionLocal

def generate_diet(user_id: int):
    """AI-style diet planner based on user goal and calories"""
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    goal = user.goal.lower()
    calories_target = user.calories_required or 2000
    today = datetime.now().date()

    # Basic food library
    foods = {
        "Breakfast": ["Oats with milk", "Boiled eggs + Toast", "Banana smoothie", "Poha", "Idli sambhar"],
        "Lunch": ["Grilled chicken + rice", "Paneer curry + roti", "Brown rice + dal", "Quinoa salad", "Vegetable khichdi"],
        "Dinner": ["Soup + salad", "Fish + veggies", "Tofu curry + roti", "Oats upma", "Veg pulao"],
        "Snack": ["Fruits", "Protein shake", "Dry fruits", "Green tea + almonds", "Greek yogurt"]
    }

    # Calorie adjustment by goal
    factor = 0.9 if goal == "weight_loss" else 1.1 if goal == "muscle_gain" else 1.0
    daily_calories = round(calories_target * factor, 0)

    meals = list(foods.keys())
    meal_ratios = {"Breakfast": 0.25, "Lunch": 0.35, "Dinner": 0.3, "Snack": 0.1}

    plans = []

    for i in range(7):  # 7-day plan
        for meal in meals:
            food = choice(foods[meal])
            cals = round(daily_calories * meal_ratios[meal])
            protein = round(cals * 0.3 / 4, 1)
            carbs = round(cals * 0.5 / 4, 1)
            fats = round(cals * 0.2 / 9, 1)

            plan = DietPlan(
                user_id=user.id,
                day=today + timedelta(days=i),
                meal_type=meal,
                food_items=food,
                calories=cals,
                protein=protein,
                carbs=carbs,
                fats=fats
            )
            db.add(plan)
            plans.append(plan)

    db.commit()
    db.close()
    return {"message": "7-day diet plan generated successfully", "user_id": user_id, "target_calories": daily_calories}
