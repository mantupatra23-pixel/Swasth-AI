from pydantic import BaseModel
from typing import Optional

class SubscriptionCreate(BaseModel):
    user_id: int
    plan_name: str
    amount: float
    currency: Optional[str] = "INR"

class SubscriptionOut(BaseModel):
    id: int
    plan_name: str
    amount: float
    currency: str
    status: str
    class Config:
        orm_mode = True
