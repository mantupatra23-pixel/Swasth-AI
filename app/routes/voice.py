from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.services.ai_chat import generate_ai_response
from app.voice.voice_utils import transcribe_audio, text_to_speech
import os, tempfile

router = APIRouter(prefix="/voice", tags=["Voice AI"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/transcribe")
async def transcribe_voice(file: UploadFile = File(...)):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.write(await file.read())
    temp.close()
    text = transcribe_audio(temp.name)
    os.unlink(temp.name)
    return {"transcribed_text": text}

@router.post("/speak")
async def speak_ai(user_id: int, message: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    ai_reply = generate_ai_response(user, message)
    text_reply = ai_reply["reply"]

    # Convert to voice
    audio_path = text_to_speech(text_reply)
    return FileResponse(audio_path, media_type="audio/mpeg", filename="response.mp3")
