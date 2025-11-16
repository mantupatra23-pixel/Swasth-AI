from fastapi import APIRouter()

router = APIRouter(prefix="/engagement", tags=["Engagement"])

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "engagement"}
