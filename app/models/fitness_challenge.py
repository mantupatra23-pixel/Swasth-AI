from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class FitnessChallenge(Base):
    __tablename__ = "fitness_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    goal_type = Column(String)  # steps, calories, workouts
    goal_value = Column(Float)
    duration_days = Column(Integer, default=7)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
