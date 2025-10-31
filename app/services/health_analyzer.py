def analyze_health(profile):
    height_m = profile["height"] / 100
    bmi = round(profile["weight"] / (height_m ** 2), 2)

    # BMR Calculation (Mifflin St Jeor Formula)
    if profile["gender"].lower() == "male":
        bmr = 88.36 + (13.4 * profile["weight"]) + (4.8 * profile["height"]) - (5.7 * profile["age"])
    else:
        bmr = 447.6 + (9.2 * profile["weight"]) + (3.1 * profile["height"]) - (4.3 * profile["age"])

    # Ideal weight (BMI target 22)
    ideal_weight = round(22 * (height_m ** 2), 1)

    # Calorie needs multiplier
    activity_factor = {
        "sedentary": 1.2,
        "active": 1.55,
        "athlete": 1.9
    }.get(profile["lifestyle"].lower(), 1.2)

    calories_required = round(bmr * activity_factor, 0)

    # Adjust for goal
    if profile["goal"] == "weight_loss":
        calories_required -= 300
    elif profile["goal"] == "muscle_gain":
        calories_required += 300

    return {
        "bmi": bmi,
        "bmr": round(bmr, 1),
        "ideal_weight": ideal_weight,
        "calories_required": calories_required
    }
