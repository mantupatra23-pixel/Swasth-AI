from pydantic import BaseModel
from datetime import datetime

class FeedOut(BaseModel):
    id: int
    title: str
    message: str
    category: str
    image_url: str | None
    created_at: datetime

    class Config:
        orm_mode = True
