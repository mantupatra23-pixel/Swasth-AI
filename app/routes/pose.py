from fastapi import APIRouter
from app.services.pose_trainer import pose_detection_live

router = APIRouter(prefix="/pose", tags=["AI Pose Trainer"])

@router.get("/detect")
def detect_pose(exercise_name: str = "pushup"):
    """
    Start real-time camera detection.
    Press 'q' to exit.
    """
    pose_detection_live(exercise_name)
    return {"message": f"Pose detection for {exercise_name} completed."}
