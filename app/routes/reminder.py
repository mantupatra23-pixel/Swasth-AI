from fastapi import APIRouter()
from app.services.reminder_service import add_reminder, get_all_reminders, run_reminders
from app.schemas.reminder import ReminderCreate

router = APIRouter(prefix="/reminder", tags=["Reminder System"])

@router.post("/add")
def create_reminder(data: ReminderCreate):
    """Add custom reminder"""
    return add_reminder(data)

@router.get("/all/{user_id}")
def list_reminders(user_id: int):
    """Get all reminders for user"""
    return get_all_reminders(user_id)

@router.get("/run")
def trigger_reminders():
    """Check and send reminders (auto-trigger)"""
    return run_reminders()
