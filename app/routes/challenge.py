from fastapi import APIRouter
from app.services.challenge_service import create_ai_challenge, join_challenge, update_progress, get_leaderboard

router = APIRouter(prefix="/challenge", tags=["AI Fitness Challenges"])

@router.post("/create")
def create_challenge():
    """AI generates new weekly challenge"""
    return create_ai_challenge()

@router.post("/join/{challenge_id}/{user_id}")
def join(challenge_id: int, user_id: int):
    """Join an active challenge"""
    return join_challenge(challenge_id, user_id)

@router.post("/progress/{challenge_id}/{user_id}")
def update(challenge_id: int, user_id: int, progress: float):
    """Update progress manually (or auto-sync via Google Fit)"""
    return update_progress(challenge_id, user_id, progress)

@router.get("/leaderboard/{challenge_id}")
def leaderboard(challenge_id: int):
    """Get challenge leaderboard"""
    return get_leaderboard(challenge_id)
