from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    day = Column(Date)
    meal_type = Column(String)  # Breakfast, Lunch, Dinner, Snack
    food_items = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
