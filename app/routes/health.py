from fastapi import APIRouter
from app.services.health_monitor import add_health_log, get_health_report
from app.schemas.health_log import HealthLogCreate

router = APIRouter(prefix="/health", tags=["Health Monitor"])

@router.post("/add")
def add_health_data(data: HealthLogCreate):
    """Add daily health vitals"""
    return add_health_log(data)

@router.get("/report/{user_id}")
def health_report(user_id: int):
    """Get weekly AI health report"""
    return get_health_report(user_id)
