from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.content_plan import ContentPlan
from app.services.hashtag_analyzer import analyze_hashtags
from datetime import datetime

celery = Celery(
    "hashtag_scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="auto_analyze_hashtags")
def auto_analyze_hashtags():
    db = SessionLocal()
    plans = db.query(ContentPlan).filter(ContentPlan.hashtags == None).all()
    if not plans:
        print("⚠️ No new posts left for hashtag analysis.")
        return

    for plan in plans:
        analyze_hashtags(plan.id)
    db.close()
    print(f"📊 Auto Hashtag Analyzer Completed at {datetime.now()}")
