from fastapi import APIRouter
from app.services.progress_visualizer import generate_visual_report

router = APIRouter(prefix="/progress", tags=["AI Progress Visualizer"])

@router.get("/visual/{user_id}")
def visual_report(user_id: int):
    """Generate visual + AI summary of user's fitness progress"""
    return generate_visual_report(user_id)
