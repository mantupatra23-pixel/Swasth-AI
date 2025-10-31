from fastapi import APIRouter
from app.services.payment_service import create_payment, verify_payment, get_plans

router = APIRouter(prefix="/payment", tags=["Payments"])

@router.get("/plans")
def plans():
    """Get all subscription plans"""
    return get_plans()

@router.post("/create/{user_id}")
def create_order(user_id: int, plan_name: str, amount: float, gateway: str = "razorpay"):
    """Create payment order"""
    return create_payment(user_id, plan_name, amount, gateway)

@router.post("/verify/{payment_id}")
def verify_order(payment_id: str, signature: str = None):
    """Verify payment success"""
    return verify_payment(payment_id, signature)
