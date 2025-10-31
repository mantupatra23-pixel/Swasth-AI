from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.feed import Feed
from app.services.social_poster import post_to_instagram, post_to_twitter
from datetime import datetime
import random

celery = Celery(
    "social_scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="post_daily_feed")
def post_daily_feed():
    db = SessionLocal()
    latest_feed = db.query(Feed).order_by(Feed.id.desc()).first()
    if not latest_feed:
        print("⚠️ No feed found to post.")
        return

    caption = latest_feed.message
    if latest_feed.title:
        caption = f"{latest_feed.title}: {caption}"

    print(f"📅 Auto-posting: {caption[:60]}...")

    # Randomly choose platform
    post_to_instagram(latest_feed.image_url, caption)
    post_to_twitter(latest_feed.image_url, caption)

    db.close()
    print(f"✅ Auto-Posted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
