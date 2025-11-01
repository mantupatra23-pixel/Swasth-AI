import os
import openai
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🎙️ Convert speech to text (via Whisper model)
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcript.text
    except Exception as e:
        return f"Error during transcription: {str(e)}"

# 🔊 Convert AI reply text to speech (using gTTS)
def text_to_speech(text, output_path="response.mp3"):
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(output_path)
        return output_path
    except Exception as e:
        return f"Error generating audio: {str(e)}"
