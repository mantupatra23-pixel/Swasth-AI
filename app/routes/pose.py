from fastapi import APIRouter()

router = APIRouter(prefix="/pose", tags=["Pose"])

@router.get("/")
def pose_root():
    return {"message": "Pose module active"}
