from fastapi import APIRouter, Header
from app.services.google_fit_service import sync_google_fit

router = APIRouter(prefix="/fit", tags=["Google Fit Sync"])

@router.post("/sync/{user_id}")
def google_fit_sync(user_id: int, authorization: str = Header(...)):
    """Sync health data from Google Fit"""
    token = authorization.replace("Bearer ", "")
    return sync_google_fit(user_id, token)
