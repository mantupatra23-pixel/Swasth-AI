import os
import openai
import redis
import json
from app.services.ai_engine import compute_bmi
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize OpenAI (for old SDK v0.28 style)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize Redis (for chat memory)
r = redis.Redis(host="redis", port=6379, db=1)

# ✅ Get user chat history
def get_chat_history(user_id: int):
    key = f"chat:{user_id}"
    data = r.get(key)
    if not data:
        return []
    return json.loads(data)

# ✅ Save chat history (limit last 3 messages)
def save_chat_history(user_id: int, history):
    key = f"chat:{user_id}"
    if len(history) > 3:
        history = history[-3:]
    r.set(key, json.dumps(history))

# ✅ Main AI Response Generator
def generate_ai_response(user, message: str):
    bmi = compute_bmi(user.weight, user.height)
    goal = user.goal or "maintain"
    history = get_chat_history(user.id)

    # Context for GPT
    context_msgs = [
        {
            "role": "system",
            "content": "You are Swasth.AI, a professional health assistant who provides personalized fitness and diet advice."
        }
    ]

    for h in history:
        context_msgs.append({"role": "user", "content": h["user"]})
        context_msgs.append({"role": "assistant", "content": h["ai"]})

    context_msgs.append({"role": "user", "content": message})

    try:
        # ✅ OpenAI API call (compatible with 0.28 SDK)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context_msgs,
            temperature=0.8,
            max_tokens=200
        )
        reply = completion.choices[0].message["content"].strip()

    except Exception as e:
        reply = f"⚠️ Offline Mode: Based on your goal ({goal}) and BMI ({bmi}), keep your daily balance consistent."

    # Save updated history
    history.append({"user": message, "ai": reply})
    save_chat_history(user.id, history)

    return {"reply": reply, "bmi": bmi, "goal": goal}
