from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from app.core.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    goal = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
