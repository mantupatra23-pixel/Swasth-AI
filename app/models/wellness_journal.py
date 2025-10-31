from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import date

class WellnessJournal(Base):
    __tablename__ = "wellness_journal"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    entry_date = Column(Date, default=date.today)
    mood = Column(String)
    content = Column(Text)
    ai_feedback = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
