from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.feed import Feed
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(
    prefix="/share",
    tags=["Social Share"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/feed/{feed_id}")
def generate_share_content(feed_id: int, db: Session = Depends(get_db)):
    feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")

    # AI-generated caption
    prompt = f"Write a short motivational Instagram caption based on: {feed.message}"

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a motivational caption generator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=80
        )
        caption = completion.choices[0].message.content

    except Exception as e:
        caption = f"{feed.message}\n\n#SwasthAI #Motivation"

    share_payload = {
        "title": feed.title,
        "message": feed.message,
        "image_url": feed.image_url,
        "caption": caption,
        "share_links": {
            "whatsapp": f"https://api.whatsapp.com/send?text={caption}",
            "telegram": f"https://t.me/share/url?url={feed.image_url}&text={caption}",
            "twitter": f"https://twitter.com/intent/tweet?text={caption}"
        }
    }

    return share_payload
