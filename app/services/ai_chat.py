import os
import redis
import openai
import json
from app.services.ai_engine import compute_bmi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI (new SDK compatible)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Redis for chat memory
r = redis.Redis(host="redis", port=6379, db=1)

# -----------------------------
# Helper functions
# -----------------------------

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

# -----------------------------
# Main AI Response Generator
# -----------------------------

def generate_ai_response(user, message: str):
    try:
        bmi = compute_bmi(user.weight, user.height)
        goal = getattr(user, "goal", "maintain")

        history = get_chat_history(user.id)

        # Context setup for GPT
        context_msgs = [
            {"role": "system", "content": "You are Swasth.AI, a professional health assistant that gives fitness, nutrition, and motivation guidance based on user BMI and goal."}
        ]

        # Add previous messages for context
        for h in history:
            context_msgs.append({"role": "user", "content": h["user"]})
            context_msgs.append({"role": "assistant", "content": h["ai"]})

        # Add new message
        context_msgs.append({"role": "user", "content": message})

        # Call GPT model
        completion = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=context_msgs,
            temperature=0.8,
            max_tokens=200
        )

        reply = completion.choices[0].message["content"].strip()

    except Exception as e:
        reply = f"⚠️ Offline Mode: Based on your goal ({goal}) and BMI ({bmi}), stay consistent with your routine. ({str(e)})"

    # Save chat history
    history.append({"user": message, "ai": reply})
    save_chat_history(user.id, history)

    return {"reply": reply, "bmi": bmi, "goal": goal}
