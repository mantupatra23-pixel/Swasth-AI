from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey, Boolean
from app.core.database import Base
from sqlalchemy.sql import func

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_name = Column(String)
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String, default="pending")   # pending/active/expired
    stripe_session_id = Column(String)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
