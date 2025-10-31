from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.services.video_trainer import generate_ai_video, get_video

router = APIRouter(prefix="/video", tags=["AI Video Trainer"])

@router.post("/generate")
def create_video(exercise_name: str):
    """Generate AI workout video"""
    return generate_ai_video(exercise_name)

@router.get("/{exercise_name}")
def get_generated_video(exercise_name: str):
    """Fetch existing video"""
    path = get_video(exercise_name)
    if not path:
        return {"error": "Video not found. Please generate first."}
    return FileResponse(path, media_type="video/mp4")
