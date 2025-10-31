from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date
from datetime import date
from app.core.database import Base

class HabitProgress(Base):
    __tablename__ = "habit_progress"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("ai_habits.id"))
    date = Column(Date, default=date.today)
    completed = Column(Boolean, default=False)
