import cv2
import mediapipe as mp
import numpy as np
from gtts import gTTS
import os
from datetime import datetime

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def analyze_pose(pose_landmarks, exercise):
    """
    Compare user pose to ideal pose for the exercise and return feedback.
    """
    feedback = "Perfect form! Keep it up 💪"
    risk = "low"

    # Example check for pushups: elbow angle, back straight
    if exercise.lower() == "pushup":
        shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        elbow = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        angle = calculate_angle(shoulder, elbow, wrist)
        if angle < 60:
            feedback = "Bend your elbows less. Keep your back straight."
            risk = "medium"
        elif angle > 160:
            feedback = "You’re overextending! Lower slightly."
            risk = "high"

    elif exercise.lower() == "squat":
        knee = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        hip = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        angle = calculate_angle(hip, knee, ankle)
        if angle < 70:
            feedback = "Go deeper in your squat 🏋️"
        elif angle > 140:
            feedback = "Don’t lock your knees."

    return feedback, risk

def calculate_angle(a, b, c):
    """
    Calculate angle between three points (a-b-c)
    """
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def pose_detection_live(exercise_name="pushup"):
    """
    Real-time pose detection with feedback and voice alert.
    """
    cap = cv2.VideoCapture(0)
    mp_pose_model = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    os.makedirs("pose_feedback", exist_ok=True)
    print("🎥 Pose Detection Active - Press 'q' to quit")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_pose_model.process(image)

        # Draw landmarks
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            feedback, risk = analyze_pose(results.pose_landmarks, exercise_name)

            cv2.putText(image, feedback, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0) if "Perfect" in feedback else (0, 0, 255), 2)

            # Optional: Speak feedback
            speak_feedback(feedback)

        cv2.imshow(f"Swasth.AI - {exercise_name.title()} Trainer", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    mp_pose_model.close()
    print("🏁 Pose Detection Ended")

def speak_feedback(text):
    """Generate speech for feedback"""
    audio_path = f"pose_feedback/voice_{datetime.now().timestamp()}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)
    os.system(f"mpg123 {audio_path} > /dev/null 2>&1")
