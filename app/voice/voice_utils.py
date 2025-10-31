import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os, uuid

def transcribe_audio(file_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except Exception as e:
        return f"Error: {str(e)}"

def text_to_speech(text: str, lang: str = "en") -> str:
    tts = gTTS(text=text, lang=lang)
    file_id = str(uuid.uuid4())
    output_path = f"/tmp/{file_id}.mp3"
    tts.save(output_path)
    return output_path
