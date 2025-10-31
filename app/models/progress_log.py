from sqlalchemy import Column, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    weight = Column(Float)
    bmi = Column(Float)
    calories_intake = Column(Float)
    calories_burned = Column(Float)
    progress_score = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
