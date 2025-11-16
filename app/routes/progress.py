from fastapi import APIRouter()
from app.services.progress_tracker import add_progress, get_weekly_report
from app.schemas.progress_log import ProgressCreate

router = APIRouter(prefix="/progress", tags=["Progress Tracker"])

@router.post("/add")
def add_user_progress(data: ProgressCreate):
    """Add daily progress log"""
    return add_progress(data)

@router.get("/weekly/{user_id}")
def get_user_weekly_progress(user_id: int):
    """Get weekly progress summary"""
    return get_weekly_report(user_id)
