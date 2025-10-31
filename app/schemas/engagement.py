from pydantic import BaseModel
from datetime import datetime

class EngagementOut(BaseModel):
    feed_id: int
    platform: str
    likes: int
    comments: int
    shares: int
    updated_at: datetime
    class Config:
        orm_mode = True
