from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class FitnessSync(Base):
    __tablename__ = "fitness_sync"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    steps = Column(Integer)
    heart_rate = Column(Float)
    calories_burned = Column(Float)
    sleep_hours = Column(Float)
    source = Column(String)  # google_fit / apple_health
    synced_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
