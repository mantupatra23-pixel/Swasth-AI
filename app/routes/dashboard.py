from fastapi import APIRouter
from app.services.dashboard_service import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["Premium Dashboard"])

@router.get("/{user_id}")
def dashboard_summary(user_id: int):
    """Get AI-powered dashboard summary"""
    return get_dashboard(user_id)
