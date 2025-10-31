from celery import Celery
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.content_plan import ContentPlan
from app.services.social_poster import post_to_instagram, post_to_twitter
from datetime import datetime
import pytz

celery = Celery(
    "auto_scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@celery.task(name="auto_post_from_planner")
def auto_post_from_planner():
    """Post scheduled content if its time has arrived."""
    db = SessionLocal()
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    plans = (
        db.query(ContentPlan)
        .filter(ContentPlan.status == "pending")
        .filter(ContentPlan.scheduled_time <= now)
        .all()
    )
    if not plans:
        print("⏰ No scheduled posts to publish now.")
        db.close()
        return

    for plan in plans:
        caption = f"{plan.title}: {plan.caption}"
        category = plan.category.lower()
        # Select default image based on category
        default_image = f"https://via.placeholder.com/1024x1024.png?text={category.capitalize()}"

        print(f"📅 Posting scheduled content: {plan.title}")

        # Post to social media
        insta = post_to_instagram(default_image, caption)
        tw = post_to_twitter(default_image, caption)

        plan.status = "posted"
        db.commit()

        print(f"✅ Posted {plan.title} on Instagram & Twitter")

    db.close()
    print(f"🎯 Auto Scheduler Completed at {now.strftime('%H:%M:%S')}")
