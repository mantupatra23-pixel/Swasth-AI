from fastapi import APIRouter()
from app.services.caption_optimizer import optimize_caption

router = APIRouter(prefix="/caption", tags=["Caption Optimizer"])

@router.get("/optimize/{plan_id}")
def caption_optimize(plan_id: int):
    """Optimize a post caption for engagement."""
    return optimize_caption(plan_id)
