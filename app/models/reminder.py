from sqlalchemy import Column, Integer, String, Time, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    type = Column(String)  # water / diet / workout / sleep
    time = Column(Time)
    message = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
