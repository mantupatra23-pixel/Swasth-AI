from typing import Dict, Any

def compute_bmi(weight: float, height: float) -> float:
    if not height or height == 0:
        return 0.0
    return round(weight / ((height/100)**2), 2)

def base_plan(goal: str, bmi: float) -> Dict[str, Any]:
    if goal == "weight_loss":
        calories = 1800 if bmi > 25 else 2000
        workouts = ["HIIT 30min", "Cardio 25min", "Yoga 30min"]
    elif goal == "muscle_gain":
        calories = 2500
        workouts = ["Strength 45min", "Core 20min", "Cardio 25min"]
    else:
        calories = 2200
        workouts = ["Yoga 30min", "Walk 30min", "Core 20min"]
    return {"calories": calories, "workouts": workouts}

def generate_plan_from_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    weight = float(profile.get("weight", 70))
    height = float(profile.get("height", 170))
    goal = profile.get("goal", "maintain")
    bmi = compute_bmi(weight, height)
    plan = base_plan(goal, bmi)
    plan["bmi"] = bmi
    plan["goal"] = goal
    plan["message"] = f"Plan generated for goal '{goal}' with BMI {bmi}"
    return plan
