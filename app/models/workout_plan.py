from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.core.database import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plan"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    day = Column(String, nullable=False)
    workout_type = Column(String, nullable=False)
    duration = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
