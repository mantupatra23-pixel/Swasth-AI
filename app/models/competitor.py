from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class Competitor(Base):
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)  # instagram / twitter
    username = Column(String)
    profile_url = Column(String)
    followers = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    last_analyzed = Column(TIMESTAMP(timezone=True), server_default=func.now())
