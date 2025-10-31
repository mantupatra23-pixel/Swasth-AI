from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, Float
from sqlalchemy.sql import func
from app.core.database import Base

class ContentPlan(Base):
    __tablename__ = "content_plan"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date)
    category = Column(String)
    title = Column(String)
    caption = Column(String)
    optimized_caption = Column(String, nullable=True)
    engagement_score = Column(Float, nullable=True)
    status = Column(String, default="pending")  # pending | posted
    scheduled_time = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    hashtags = Column(String, nullable=True)
    hashtag_score = Column(Float, nullable=True)
