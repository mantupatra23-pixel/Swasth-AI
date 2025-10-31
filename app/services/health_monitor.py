from app.models.health_log import HealthLog
from app.core.database import SessionLocal
from datetime import datetime, timedelta

def calculate_risk(bp_sys, bp_dia, sugar, heart, sleep):
    """AI-based basic health risk scoring"""
    score = 100

    # BP range check
    if bp_sys > 130 or bp_dia > 85:
        score -= 15
    elif bp_sys < 100 or bp_dia < 60:
        score -= 10

    # Sugar check
    if sugar > 125:
        score -= 20
    elif sugar < 70:
        score -= 10

    # Heart rate
    if heart > 100 or heart < 50:
        score -= 15

    # Sleep hours
    if sleep < 6:
        score -= 10
    elif sleep > 9:
        score -= 5

    return max(0, min(100, round(score, 1)))


def add_health_log(data):
    db = SessionLocal()
    risk = calculate_risk(
        data.systolic_bp, data.diastolic_bp, data.sugar_level, data.heart_rate, data.sleep_hours
    )

    log = HealthLog(
        user_id=data.user_id,
        systolic_bp=data.systolic_bp,
        diastolic_bp=data.diastolic_bp,
        sugar_level=data.sugar_level,
        heart_rate=data.heart_rate,
        sleep_hours=data.sleep_hours,
        risk_score=risk
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    db.close()

    return {"message": "Health data added successfully", "risk_score": risk}


def get_health_report(user_id: int):
    db = SessionLocal()
    last_7_days = datetime.now() - timedelta(days=7)
    logs = db.query(HealthLog).filter(HealthLog.user_id == user_id, HealthLog.created_at >= last_7_days).all()

    if not logs:
        db.close()
        return {"message": "No data for this week"}

    avg_bp_sys = sum([x.systolic_bp for x in logs]) / len(logs)
    avg_bp_dia = sum([x.diastolic_bp for x in logs]) / len(logs)
    avg_sugar = sum([x.sugar_level for x in logs]) / len(logs)
    avg_heart = sum([x.heart_rate for x in logs]) / len(logs)
    avg_sleep = sum([x.sleep_hours for x in logs]) / len(logs)
    avg_risk = sum([x.risk_score for x in logs]) / len(logs)

    # AI health interpretation
    if avg_risk > 80:
        condition = "Excellent"
        suggestion = "Keep up the great lifestyle! Maintain balanced diet and regular exercise."
    elif avg_risk > 60:
        condition = "Good"
        suggestion = "Doing well! Try adding more consistent sleep and hydration."
    elif avg_risk > 40:
        condition = "Needs Attention"
        suggestion = "Slight imbalance noticed. Review your diet and sleep routine."
    else:
        condition = "Critical"
        suggestion = "High risk detected. Please consult a doctor immediately."

    db.close()

    return {
        "user_id": user_id,
        "avg_bp": f"{round(avg_bp_sys,1)}/{round(avg_bp_dia,1)} mmHg",
        "avg_sugar": round(avg_sugar,1),
        "avg_heart_rate": round(avg_heart,1),
        "avg_sleep": round(avg_sleep,1),
        "avg_risk": round(avg_risk,1),
        "condition": condition,
        "suggestion": suggestion
    }
