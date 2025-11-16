from fastapi import APIRouter()
from app.services.cloud_sync_service import backup_user_data, restore_user_data

router = APIRouter(prefix="/cloud", tags=["AI Cloud Sync"])

@router.post("/backup/{user_id}")
def backup_data(user_id: int):
    """Backup all user data to cloud"""
    return backup_user_data(user_id)

@router.get("/restore/{user_id}")
def restore_data(user_id: int, filename: str):
    """Restore user data from backup file"""
    return restore_user_data(user_id, filename)
