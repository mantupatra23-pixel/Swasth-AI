import os
from openai import OpenAI
from app.services.ai_engine import compute_bmi
from dotenv import load_dotenv
import redis, json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
r = redis.Redis(host="redis", port=6379, db=1)

def get_chat_history(user_id: int):
    key = f"chat:{user_id}"
    data = r.get(key)
    if not data:
        return []
    return json.loads(data)

def save_chat_history(user_id: int, history):
    key = f"chat:{user_id}"
    if len(history) > 3:  # keep only last 3 messages
        history = history[-3:]
    r.set(key, json.dumps(history))

def generate_ai_response(user, message: str):
    # Fetch basic context
    bmi = compute_bmi(user.weight, user.height)
    goal = user.goal or "maintain"
    history = get_chat_history(user.id)
    context_msgs = [
        {"role": "system", "content": f"You are Swasth.AI, a professional health & fitness coach. User’s goal: {goal}, BMI: {bmi}."}
    ]
    for h in history:
        context_msgs.append({"role": "user", "content": h["user"]})
        context_msgs.append({"role": "assistant", "content": h["ai"]})
    context_msgs.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=context_msgs,
            temperature=0.8,
            max_tokens=200
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = f"⚠️ Offline mode: Based on your goal ({goal}) and BMI ({bmi}), I suggest focusing on balanced meals and 30 mins of exercise daily."

    # Update memory
    history.append({"user": message, "ai": reply})
    save_chat_history(user.id, history)

    return {"reply": reply, "bmi": bmi, "goal": goal}
