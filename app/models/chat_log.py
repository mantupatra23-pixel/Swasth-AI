from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.sql import func
from app.core.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    user_message = Column(Text)
    ai_response = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
