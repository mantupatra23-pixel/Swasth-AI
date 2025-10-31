import os
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_video(exercise_name: str):
    os.makedirs("videos", exist_ok=True)
    filename = f"videos/{exercise_name.replace(' ', '_')}.mp4"

    # Step 1: Generate exercise instructions using GPT
    try:
        prompt = f"Describe a {exercise_name} workout in 5 simple steps for beginners."
        res = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a professional fitness instructor."},
                      {"role": "user", "content": prompt}]
        )
        steps = res.choices[0].message.content.strip()
    except Exception as e:
        steps = "Step 1: Warm up\nStep 2: Perform exercise slowly\nStep 3: Maintain posture\nStep 4: Breathe properly\nStep 5: Cool down."

    # Step 2: Generate audio using gTTS
    tts = gTTS(text=f"Here’s your {exercise_name} guide. {steps}", lang="en", slow=False)
    audio_path = f"videos/{exercise_name.replace(' ', '_')}.mp3"
    tts.save(audio_path)

    # Step 3: Generate basic video using text overlays
    step_lines = steps.split('\n')
    clips = []

    for i, line in enumerate(step_lines):
        text = TextClip(line, fontsize=40, color='white', bg_color='black', size=(720, 480))
        clip = text.set_duration(3)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    background = ColorClip(size=(720, 480), color=(0, 0, 0), duration=video.duration)
    final = CompositeVideoClip([background, video])
    final.write_videofile(filename, fps=24, codec='libx264', audio=audio_path)

    return {"message": f"AI workout video for {exercise_name} created!", "video_path": filename}


def get_video(exercise_name: str):
    path = f"videos/{exercise_name.replace(' ', '_')}.mp4"
    if os.path.exists(path):
        return path
    return None
