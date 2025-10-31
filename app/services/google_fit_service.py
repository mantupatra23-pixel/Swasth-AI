import requests, os
from datetime import datetime, timedelta
from app.models.fitness_sync import FitnessSync
from app.models.health_log import HealthLog
from app.core.database import SessionLocal

GOOGLE_FIT_URL = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

def sync_google_fit(user_id: int, token: str):
    """
    Fetch data from Google Fit and update health log + sync table.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    end_time = int(datetime.utcnow().timestamp() * 1000)
    start_time = int((datetime.utcnow() - timedelta(days=1)).timestamp() * 1000)

    payload = {
        "aggregateBy": [
            {"dataTypeName": "com.google.step_count.delta"},
            {"dataTypeName": "com.google.calories.expended"},
            {"dataTypeName": "com.google.heart_rate.bpm"},
            {"dataTypeName": "com.google.sleep.segment"}
        ],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }

    res = requests.post(GOOGLE_FIT_URL, headers=headers, json=payload)

    if res.status_code != 200:
        return {"error": "Failed to fetch Google Fit data", "status": res.status_code}

    data = res.json().get("bucket", [])
    if not data:
        return {"message": "No data available"}

    total_steps = 0
    total_calories = 0
    avg_heart = 0
    sleep_hours = 0

    for bucket in data:
        for dataset in bucket.get("dataset", []):
            points = dataset.get("point", [])
            for p in points:
                t = p["dataTypeName"]
                vals = p["value"][0].get("intVal") or p["value"][0].get("fpVal", 0)
                if "step" in t:
                    total_steps += vals
                elif "calories" in t:
                    total_calories += vals
                elif "heart" in t:
                    avg_heart += vals
                elif "sleep" in t:
                    sleep_hours += 7  # approximate (Google Fit sleep segment data)

    avg_heart = round(avg_heart / 3, 1) if avg_heart > 0 else 72

    # Save to DB
    db = SessionLocal()
    sync = FitnessSync(
        user_id=user_id,
        steps=int(total_steps),
        heart_rate=avg_heart,
        calories_burned=round(total_calories, 2),
        sleep_hours=sleep_hours,
        source="google_fit"
    )
    db.add(sync)
    db.commit()

    # Update health log
    health = HealthLog(
        user_id=user_id,
        systolic_bp=120,
        diastolic_bp=80,
        sugar_level=100,
        heart_rate=avg_heart,
        sleep_hours=sleep_hours,
        risk_score=min(100, 90 + (sleep_hours - 6) * 2)
    )
    db.add(health)
    db.commit()
    db.close()

    return {
        "message": "Google Fit data synced successfully",
        "steps": total_steps,
        "heart_rate": avg_heart,
        "calories_burned": total_calories,
        "sleep_hours": sleep_hours
    }
