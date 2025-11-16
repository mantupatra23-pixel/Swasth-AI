from fastapi import APIRouter()
from app.services.journal_service import add_journal_entry, get_today_entry, get_ai_insight
from app.schemas.journal import JournalEntry

router = APIRouter(prefix="/journal", tags=["AI Wellness Journal"])

@router.post("/add")
def add_entry(data: JournalEntry):
    """Add daily journal entry with AI feedback"""
    return add_journal_entry(data.user_id, data.mood, data.content)

@router.get("/today/{user_id}")
def today_entry(user_id: int):
    """Fetch today’s journal entry"""
    return get_today_entry(user_id)

@router.get("/insight/{user_id}")
def ai_weekly_insight(user_id: int):
    """Generate weekly AI insight"""
    return get_ai_insight(user_id)
