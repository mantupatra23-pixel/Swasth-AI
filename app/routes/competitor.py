from fastapi import APIRouter
from app.services.competitor_analyzer import analyze_competitors

router = APIRouter(prefix="/competitor", tags=["Competitor Analyzer"])

@router.get("/analyze")
def competitor_analysis():
    """AI analysis of top competitor content strategies."""
    return analyze_competitors()
