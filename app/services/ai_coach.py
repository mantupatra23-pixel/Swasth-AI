from app.models.chat_log import ChatLog
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_coach(user_id: int, message: str):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()

    if not user:
        db.close()
        return {"error": "User profile not found"}

    # Context awareness
    user_context = (
        f"User Profile: {user.name}, Age {user.age}, Goal: {user.goal}, "
        f"Height: {user.height}cm, Weight: {user.weight}kg, Lifestyle: {user.lifestyle}. "
        "You are their AI fitness & diet coach. Respond clearly, in short actionable steps."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a professional health and fitness AI coach."},
                {"role": "assistant", "content": user_context},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = "I'm sorry, I couldn’t process your request right now. Please try again."

    # Store chat
    log = ChatLog(user_id=user.id, user_message=message, ai_response=reply)
    db.add(log)
    db.commit()
    db.close()

    return {"reply": reply, "created_at": datetime.now().isoformat()}
