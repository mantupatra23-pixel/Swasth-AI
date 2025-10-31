from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    user_id: int
    content: str
    image_url: str | None = None

class CommentCreate(BaseModel):
    user_id: int
    comment: str

class PostOut(BaseModel):
    id: int
    user_id: int
    content: str
    image_url: str | None
    likes: int
    created_at: datetime

    class Config:
        orm_mode = True
