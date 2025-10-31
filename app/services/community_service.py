from app.models.community_post import CommunityPost
from app.models.community_comment import CommunityComment
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os, random

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def add_post(data):
    db = SessionLocal()
    post = CommunityPost(user_id=data.user_id, content=data.content, image_url=data.image_url)
    db.add(post)
    db.commit()
    db.refresh(post)
    db.close()
    return {"message": "Post created successfully", "post_id": post.id}

def get_feed():
    db = SessionLocal()
    posts = db.query(CommunityPost).order_by(CommunityPost.created_at.desc()).limit(50).all()
    db.close()
    return posts

def add_comment(post_id: int, user_id: int, comment: str):
    db = SessionLocal()
    c = CommunityComment(post_id=post_id, user_id=user_id, comment=comment)
    db.add(c)
    db.commit()
    db.close()
    return {"message": "Comment added successfully"}

def ai_auto_encouragement():
    """AI auto-motivation feature"""
    db = SessionLocal()
    users = db.query(HealthProfile).all()
    low_users = random.sample(users, min(2, len(users)))

    for user in low_users:
        msg = f"Keep going {user.name}! Small steps every day make big results 💪"
        post = CommunityPost(user_id=user.id, content=msg)
        db.add(post)
    db.commit()
    db.close()
    print("🤖 AI Encouragement Posts Created ✅")
