from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    day = Column(Date)
    category = Column(String)  # strength/cardio/yoga etc.
    workout_name = Column(String)
    duration_min = Column(Integer)
    calories_burn = Column(Float)
    intensity = Column(String)  # low/medium/high
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
