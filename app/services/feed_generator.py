import openai
import os
from dotenv import load_dotenv
import random
from app.services.image_generator import generate_feed_image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

categories = ["motivation", "nutrition", "workout", "mindfulness"]

def generate_feed():
    cat = random.choice(categories)
    prompt = f"Generate a short motivational or fitness tip (2 sentences) for {cat}."

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a health and motivation expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        msg = completion.choices[0].message["content"].strip()
    except Exception:
        msg = "Stay strong and consistent. Every step counts toward your health goals!"

    # Generate image
    image_url = generate_feed_image(msg, cat)

    return {
        "title": cat.capitalize() + " Tip",
        "message": msg,
        "category": cat,
        "image_url": image_url
    }
