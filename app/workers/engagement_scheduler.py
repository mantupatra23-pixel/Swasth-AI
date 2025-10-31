from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.engagement import Engagement
from app.services.engagement_tracker import update_engagement
from datetime import datetime

celery = Celery(
    "engagement_scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="track_engagement")
def track_engagement():
    db = SessionLocal()
    all_posts = db.query(Engagement).all()
    if not all_posts:
        print("⚠️ No posts to track.")
        return

    for e in all_posts:
        update_engagement(e.feed_id, e.platform, e.post_id)
    db.close()
    print(f"📊 Engagement check done at {datetime.now()}")
