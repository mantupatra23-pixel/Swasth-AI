from fastapi import APIRouter
from app.services.trend_analyzer import analyze_trends

router = APIRouter(prefix="/analytics", tags=["Trend Analyzer"])

@router.get("/trends")
def get_trends():
    """AI-powered engagement trend summary."""
    return analyze_trends()
