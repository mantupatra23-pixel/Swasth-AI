from pydantic import BaseModel
from datetime import date, datetime

class PlanOut(BaseModel):
    id: int
    day: date
    category: str
    title: str
    caption: str
    status: str
    scheduled_time: datetime
    class Config:
        orm_mode = True
