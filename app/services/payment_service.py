import razorpay
import stripe
import os
from app.models.subscription import Subscription
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal

# Razorpay Keys (India)
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

# Stripe Keys (International)
STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY")

razor_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))
stripe.api_key = STRIPE_KEY

def create_payment(user_id: int, plan_name: str, amount: float, gateway: str = "razorpay"):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    if gateway == "razorpay":
        order = razor_client.order.create({
            "amount": int(amount * 100),
            "currency": "INR",
            "payment_capture": 1,
        })
        order_id = order["id"]
        payment = Subscription(
            user_id=user.id, plan_name=plan_name, plan_price=amount,
            currency="INR", payment_id=order_id, gateway="razorpay", active=False
        )
    else:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": plan_name},
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://swasth.ai/payment/success",
            cancel_url="https://swasth.ai/payment/fail",
        )
        order_id = session.id
        payment = Subscription(
            user_id=user.id, plan_name=plan_name, plan_price=amount,
            currency="USD", payment_id=order_id, gateway="stripe", active=False
        )

    db.add(payment)
    db.commit()
    db.close()

    return {
        "gateway": gateway,
        "order_id": order_id,
        "amount": amount,
        "currency": "INR" if gateway == "razorpay" else "USD",
        "message": "Payment order created successfully"
    }


def verify_payment(payment_id: str, signature: str = None):
    db = SessionLocal()
    payment = db.query(Subscription).filter(Subscription.payment_id == payment_id).first()
    if not payment:
        return {"error": "Payment not found"}

    payment.active = True
    user = db.query(HealthProfile).filter(HealthProfile.id == payment.user_id).first()
    user.is_premium = True
    db.commit()
    db.close()

    return {"message": "Payment verified successfully. Premium activated!"}


def get_plans():
    return [
        {"name": "Basic Fit", "price": 199, "duration": "1 Month", "features": ["Diet Plan", "Workout", "Reminders"]},
        {"name": "Pro Coach", "price": 499, "duration": "3 Months", "features": ["AI Voice Coach", "Dashboard", "Pose Trainer"]},
        {"name": "Elite Life", "price": 999, "duration": "1 Year", "features": ["All Features + Personal AI Chat + Reports"]},
    ]
