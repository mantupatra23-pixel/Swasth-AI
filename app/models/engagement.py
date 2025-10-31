from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from app.core.database import Base
from sqlalchemy.sql import func

class Engagement(Base):
    __tablename__ = "feed_metrics"
    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    platform = Column(String)  # instagram/twitter
    post_id = Column(String)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
