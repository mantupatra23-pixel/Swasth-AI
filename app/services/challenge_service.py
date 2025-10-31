import os
from datetime import datetime, timedelta
from openai import OpenAI
from app.models.fitness_challenge import FitnessChallenge
from app.models.challenge_participant import ChallengeParticipant
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_ai_challenge():
    """AI generates a new challenge every week"""
    db = SessionLocal()

    prompt = """
    Generate a weekly fitness challenge for a mixed audience.
    Include one of these types: steps, calories, or workouts.
    Give a short motivational title and set a realistic goal value.
    Output format:
    Title | Type | Value
    """

    try:
        result = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        text = result.choices[0].message.content.strip()
    except Exception:
        text = "Swasth.AI Step Surge | steps | 30000"

    title, goal_type, goal_value = [t.strip() for t in text.split("|")]
    challenge = FitnessChallenge(title=title, goal_type=goal_type, goal_value=float(goal_value))
    db.add(challenge)
    db.commit()
    db.close()

    return {"message": "AI Challenge created", "title": title, "goal_type": goal_type, "goal_value": goal_value}


def join_challenge(challenge_id: int, user_id: int):
    db = SessionLocal()
    exists = db.query(ChallengeParticipant).filter(
        ChallengeParticipant.challenge_id == challenge_id,
        ChallengeParticipant.user_id == user_id
    ).first()
    if exists:
        return {"message": "Already joined"}

    participant = ChallengeParticipant(challenge_id=challenge_id, user_id=user_id)
    db.add(participant)
    db.commit()
    db.close()
    return {"message": "Joined challenge successfully"}


def update_progress(challenge_id: int, user_id: int, new_progress: float):
    db = SessionLocal()
    record = db.query(ChallengeParticipant).filter(
        ChallengeParticipant.challenge_id == challenge_id,
        ChallengeParticipant.user_id == user_id
    ).first()
    if not record:
        return {"error": "User not in challenge"}

    record.progress = new_progress
    if new_progress >= get_goal_value(challenge_id):
        record.completed = True

    db.commit()
    db.close()
    return {"message": "Progress updated"}


def get_goal_value(challenge_id):
    db = SessionLocal()
    goal = db.query(FitnessChallenge).filter(FitnessChallenge.id == challenge_id).first()
    db.close()
    return goal.goal_value


def get_leaderboard(challenge_id: int):
    db = SessionLocal()
    participants = db.query(ChallengeParticipant).filter(ChallengeParticipant.challenge_id == challenge_id).order_by(
        ChallengeParticipant.progress.desc()).all()

    leaderboard = [
        {"rank": i + 1, "user_id": p.user_id, "progress": p.progress, "completed": p.completed}
        for i, p in enumerate(participants)
    ]

    db.close()
    return leaderboard
