import os
import base64
import openai
from app.core.supabase_client import supabase
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def upload_to_supabase(local_path: str, file_name: str) -> str:
    """Upload file to Supabase and return public URL."""
    bucket = os.getenv("SUPABASE_BUCKET", "feed-images")
    try:
        with open(local_path, "rb") as f:
            supabase.storage.from_(bucket).upload(file_name, f)
            public_url = supabase.storage.from_(bucket).get_public_url(file_name)
            print(f"✅ Uploaded to Supabase: {public_url}")
            return public_url
    except Exception as e:
        print(f"⚠️ Supabase upload failed: {e}")
        return "https://via.placeholder.com/1024x1024.png?text=Swasth.AI+Feed"


def generate_feed_image(prompt_text: str, category: str) -> str:
    """Generate motivational image using OpenAI DALL·E & upload to Supabase."""
    scene_prompt = f"Create a clean, inspirational {category} poster about: {prompt_text}"
    try:
        result = openai.images.generate(
            model="gpt-image-1",
            prompt=scene_prompt,
            size="1024x1024"
        )
        image_base64 = result.data[0].b64_json
        img_data = base64.b64decode(image_base64)

        file_name = f"{category}_{os.urandom(4).hex()}.png"
        local_path = f"/tmp/{file_name}"

        with open(local_path, "wb") as f:
            f.write(img_data)

        # Upload to Supabase
        image_url = upload_to_supabase(local_path, file_name)
        os.remove(local_path)
        return image_url

    except Exception as e:
        print(f"⚠️ Image generation failed: {e}")
        return "https://via.placeholder.com/1024x1024.png?text=Swasth.AI+Feed"
