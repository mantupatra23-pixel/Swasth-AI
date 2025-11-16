from fastapi import APIRouter()
from app.services.hashtag_analyzer import analyze_hashtags

router = APIRouter(prefix="/hashtag", tags=["Hashtag Analyzer"])

@router.get("/analyze/{plan_id}")
def analyze(plan_id: int):
    """Analyze and optimize hashtags for a given content plan."""
    return analyze_hashtags(plan_id)
