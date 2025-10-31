from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    goal = Column(String)   # weight_loss, muscle_gain, maintain
    lifestyle = Column(String)  # sedentary, active, athlete
    bmi = Column(Float, nullable=True)
    bmr = Column(Float, nullable=True)
    ideal_weight = Column(Float, nullable=True)
    calories_required = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
