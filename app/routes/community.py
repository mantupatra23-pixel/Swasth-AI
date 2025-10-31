from fastapi import APIRouter
from app.services.community_service import add_post, get_feed, add_comment, ai_auto_encouragement
from app.schemas.community import PostCreate, CommentCreate

router = APIRouter(prefix="/community", tags=["Community"])

@router.post("/post")
def create_post(data: PostCreate):
    """Create a new community post"""
    return add_post(data)

@router.get("/feed")
def list_posts():
    """Get latest community posts"""
    return get_feed()

@router.post("/comment/{post_id}")
def comment_post(post_id: int, data: CommentCreate):
    """Add comment on a post"""
    return add_comment(post_id, data.user_id, data.comment)

@router.get("/ai/encourage")
def ai_encouragement():
    """AI auto motivational post generator"""
    ai_auto_encouragement()
    return {"message": "AI encouragement posts generated"}
