import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_feed_image(prompt_text: str, category: str) -> str:
    """
    Generate motivational image using OpenAI DALL·E or fallback placeholder.
    """
    try:
        # Create visual description
        scene_prompt = f"Minimalistic motivational poster about {category}. Text on image: '{prompt_text[:120]}'"
        image = client.images.generate(
            model="gpt-image-1",
            prompt=scene_prompt,
            size="1024x1024"
        )
        image_base64 = image.data[0].b64_json
        img_data = base64.b64decode(image_base64)

        save_path = f"/tmp/feed_{category}.png"
        with open(save_path, "wb") as f:
            f.write(img_data)

        print(f"✅ Generated AI feed image for category: {category}")
        return save_path
    except Exception as e:
        print(f"⚠️ Image generation failed: {e}")
        # fallback placeholder
        return "https://via.placeholder.com/1024x1024.png?text=Swasth.AI+Motivational+Feed"
