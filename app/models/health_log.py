from sqlalchemy import Column, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    systolic_bp = Column(Float)       # upper value
    diastolic_bp = Column(Float)      # lower value
    sugar_level = Column(Float)       # fasting sugar
    heart_rate = Column(Float)        # bpm
    sleep_hours = Column(Float)       # per day
    risk_score = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
