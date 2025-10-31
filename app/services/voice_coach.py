import os
from fastapi import UploadFile
from app.models.chat_log import ChatLog
from app.models.health_profile import HealthProfile
from app.core.database import SessionLocal
from openai import OpenAI
from gtts import gTTS
from datetime import datetime
from pydub import AudioSegment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def voice_to_text(audio_file: UploadFile):
    """Convert speech → text using Whisper"""
    try:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-tts",
            file=audio_file.file
        )
        return transcript.text.strip()
    except Exception as e:
        return "Error converting speech to text."

def text_to_voice(text: str, filename: str):
    """Convert text → voice using gTTS"""
    tts = gTTS(text=text, lang="en", slow=False)
    filepath = f"temp/{filename}.mp3"
    os.makedirs("temp", exist_ok=True)
    tts.save(filepath)
    return filepath

def chat_voice_coach(user_id: int, audio: UploadFile):
    db = SessionLocal()
    user = db.query(HealthProfile).filter(HealthProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    question = voice_to_text(audio)

    # AI Chat (with context)
    context = (
        f"You are {user.name}'s AI health coach. Age: {user.age}, Goal: {user.goal}, "
        f"Lifestyle: {user.lifestyle}. Speak in short and friendly motivational tone."
    )

    try:
        reply = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        ).choices[0].message.content
    except Exception as e:
        reply = "Sorry, I couldn't process that."

    # Convert reply to voice
    filename = f"voice_reply_{datetime.now().timestamp()}"
    audio_path = text_to_voice(reply, filename)

    # Save chat log
    log = ChatLog(user_id=user.id, user_message=question, ai_response=reply)
    db.add(log)
    db.commit()
    db.close()

    return {"text_reply": reply, "audio_file": audio_path}
