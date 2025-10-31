from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    goal: Optional[str] = "maintain"

class UserOut(UserCreate):
    id: int
    class Config:
        orm_mode = True
