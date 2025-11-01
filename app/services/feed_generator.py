from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from app.services.image_generator import generate_feed_image

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

categories = ["motivation", "nutrition", "workout", "mindfulness"]

def generate_feed():
    cat = random.choice(categories)
    prompt = f"Generate a short motivational or fitness tip (2 sentences) for {cat}."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a health & motivation expert"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        msg = completion.choices[0].message.content.strip()
    except Exception:
        msg = "Keep your body active and your mind strong – consistency builds strength."

    # Generate image
    image_url = generate_feed_image(msg, cat)

    return {
        "title": cat.capitalize() + " Tip",
        "message": msg,
        "category": cat,
        "image_url": image_url
    }
