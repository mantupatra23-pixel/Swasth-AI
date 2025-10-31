from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.health_profile import HealthProfile
from app.schemas.health_profile import HealthProfileCreate, HealthProfileOut
from app.services.health_analyzer import analyze_health

router = APIRouter(prefix="/user", tags=["Health Profile"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-profile", response_model=HealthProfileOut)
def create_profile(data: HealthProfileCreate, db: Session = Depends(get_db)):
    health_data = data.dict()
    analysis = analyze_health(health_data)
    new_user = HealthProfile(**health_data, **analysis)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
