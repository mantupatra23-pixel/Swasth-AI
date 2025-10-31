from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.content_plan import ContentPlan
from app.services.caption_optimizer import optimize_caption
from datetime import datetime

celery = Celery(
    "caption_scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="auto_optimize_captions")
def auto_optimize_captions():
    db = SessionLocal()
    plans = db.query(ContentPlan).filter(ContentPlan.optimized_caption == None).all()
    if not plans:
        print("⚠️ No captions left to optimize.")
        return

    for p in plans:
        optimize_caption(p.id)
    db.close()
    print(f"🧠 Auto Caption Optimization Completed at {datetime.now()}")
