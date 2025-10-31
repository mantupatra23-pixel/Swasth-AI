from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.auth import create_token, verify_password, hash_password
from app.models.admin import Admin
from app.models.user import User
from app.models.subscription import Subscription

router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Login ---
@router.post("/login")
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_token({"sub": admin.username})
    return {"token": token}

# --- Register (one-time setup) ---
@router.post("/register")
def create_admin(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(Admin).filter(Admin.username == username).first():
        raise HTTPException(status_code=400, detail="Admin exists")
    admin = Admin(username=username, password_hash=hash_password(password))
    db.add(admin)
    db.commit()
    return {"message": "Admin created"}

# --- Stats ---
@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    users = db.query(User).count()
    active_subs = db.query(Subscription).filter(Subscription.status == "active").count()
    revenue = (
        db.query(Subscription)
        .filter(Subscription.status == "active")
        .with_entities(Subscription.amount)
        .all()
    )
    total_rev = sum([r[0] for r in revenue]) if revenue else 0
    return {
        "total_users": users,
        "active_subscriptions": active_subs,
        "total_revenue": total_rev
    }

# --- List users ---
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return [
        {"id": u.id, "name": u.name, "goal": u.goal, "weight": u.weight}
        for u in db.query(User).all()
    ]

# --- List subscriptions ---
@router.get("/subscriptions")
def get_subscriptions(db: Session = Depends(get_db)):
    subs = db.query(Subscription).all()
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "plan": s.plan_name,
            "amount": s.amount,
            "status": s.status
        }
        for s in subs
    ]
