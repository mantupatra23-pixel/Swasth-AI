from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut
import stripe, os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/subscription", tags=["subscription"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=SubscriptionOut)
def create_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db)):
    sub = Subscription(**payload.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

@router.post("/checkout")
def checkout_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db)):
    try:
        checkout = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": payload.currency.lower(),
                    "product_data": {"name": payload.plan_name},
                    "unit_amount": int(payload.amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://swasth-ai.onrender.com/success",
            cancel_url="https://swasth-ai.onrender.com/cancel",
        )
        sub = Subscription(
            user_id=payload.user_id,
            plan_name=payload.plan_name,
            amount=payload.amount,
            currency=payload.currency,
            stripe_session_id=checkout["id"],
            status="pending"
        )
        db.add(sub)
        db.commit()
        return {"checkout_url": checkout.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, sig, endpoint_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        sub = db.query(Subscription).filter(
            Subscription.stripe_session_id == session["id"]
        ).first()
        if sub:
            sub.status = "active"
            sub.is_active = True
            db.commit()
    return {"status": "success"}

@router.get("/status/{user_id}")
def get_status(user_id: int, db: Session = Depends(get_db)):
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .order_by(Subscription.id.desc())
        .first()
    )
    if not sub:
        raise HTTPException(status_code=404, detail="No subscription found")
    return {
        "user_id": sub.user_id,
        "plan": sub.plan_name,
        "amount": sub.amount,
        "status": sub.status,
        "active": sub.is_active,
    }
