from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.feed import Feed
from app.services.feed_generator import generate_feed
import datetime

# Celery configuration (Redis broker + backend)
celery = Celery(
    "swasthai_scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# ✅ Link Celery Beat schedule config
celery.config_from_object("app.workers.celeryconfig")

# Database session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="generate_daily_feed")
def generate_daily_feed():
    """Automatic daily feed generation at 7 AM IST"""
    db = SessionLocal()
    try:
        feed_data = generate_feed()
        feed = Feed(**feed_data)
        db.add(feed)
        db.commit()
        print(f"✅ {datetime.datetime.now()} — New daily feed generated: {feed_data['title']}")
        return feed_data
    except Exception as e:
        print(f"❌ Feed generation failed: {e}")
    finally:
        db.close()
