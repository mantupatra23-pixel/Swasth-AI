import os
import random
import openai
from app.services.image_generator import generate_feed_image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Predefined categories for motivational or fitness content
categories = ["motivation", "nutrition", "workout", "mindfulness"]

def generate_feed():
    """
    Generates a short motivational or fitness tip,
    uses OpenAI GPT model for text generation,
    and an image generator for visual feed content.
    """
    cat = random.choice(categories)
    prompt = f"Generate a short motivational or fitness tip (2 sentences) for category: {cat}."

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a health and motivation coach creating concise, powerful tips."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.8
        )

        msg = completion.choices[0].message["content"].strip()

    except Exception as e:
        msg = f"Stay strong and consistent in your {cat} goals! ({str(e)})"

    # Generate feed image based on message and category
    image_url = generate_feed_image(msg, cat)

    return {
        "title": cat.capitalize() + " Tip",
        "message": msg,
        "category": cat,
        "image_url": image_url
    }
