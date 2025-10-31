from sqlalchemy import Column, Integer, String, JSON, ForeignKey, TIMESTAMP
from app.core.database import Base
from sqlalchemy.sql import func

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    source = Column(String)
    plan_json = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
