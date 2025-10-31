from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.feed import Feed
from app.schemas.feed import FeedOut
from app.services.feed_generator import generate_feed
from datetime import datetime, timedelta

router = APIRouter(prefix="/feed", tags=["Feed"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate", response_model=FeedOut)
def generate_daily_feed(db: Session = Depends(get_db)):
    feed_data = generate_feed()
    feed = Feed(**feed_data)
    db.add(feed)
    db.commit()
    db.refresh(feed)
    return feed

@router.get("/today", response_model=FeedOut)
def get_today_feed(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    latest = db.query(Feed).order_by(Feed.id.desc()).first()
    if not latest:
        return {"message": "No feed found yet"}
    return latest

@router.get("/all")
def get_all_feeds(db: Session = Depends(get_db)):
    feeds = db.query(Feed).order_by(Feed.id.desc()).limit(50).all()
    return feeds
