from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class AIHabit(Base):
    __tablename__ = "ai_habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    title = Column(String)
    description = Column(String)
    frequency = Column(String)  # daily / weekly
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
