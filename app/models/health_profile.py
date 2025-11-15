from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    is_premium = Column(Boolean, default=False)
    blood_pressure = Column(String, nullable=True)
    sugar_level = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    height = Column(String, nullable=True)
    bmi = Column(String, nullable=True)
    last_updated = Column(String, nullable=True)
