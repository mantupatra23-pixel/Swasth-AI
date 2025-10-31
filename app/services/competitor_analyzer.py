import requests, os, random
from app.core.database import SessionLocal
from app.models.competitor import Competitor
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Mock Competitor Data (for now)
MOCK_COMPETITORS = [
    {
        "platform": "instagram",
        "username": "fitlife_hub",
        "profile_url": "https://instagram.com/fitlife_hub",
        "followers": 145000,
        "posts": [
            {"caption": "Push your limits 💪 #MotivationMonday", "likes": 5300, "comments": 210},
            {"caption": "Fuel your body with clean energy 🌿", "likes": 4100, "comments": 145},
        ],
    },
    {
        "platform": "twitter",
        "username": "thefitnessguru",
        "profile_url": "https://twitter.com/thefitnessguru",
        "followers": 89000,
        "posts": [
            {"caption": "Discipline beats motivation every time.", "likes": 1500, "comments": 110},
            {"caption": "You are one workout away from a good mood.", "likes": 2400, "comments": 190},
        ],
    },
]

def analyze_competitors():
    """Analyze top competitors and summarize their strategy."""
    db = SessionLocal()

    # Simulate competitor insert/update
    for comp in MOCK_COMPETITORS:
        exists = db.query(Competitor).filter(Competitor.username == comp["username"]).first()
        if not exists:
            db.add(
                Competitor(
                    platform=comp["platform"],
                    username=comp["username"],
                    profile_url=comp["profile_url"],
                    followers=comp["followers"],
                    engagement_rate=random.uniform(3.5, 6.5),
                )
            )
    db.commit()

    # Prepare analysis prompt for AI
    prompt = (
        "You are a social media intelligence system. Analyze the competitors' recent content "
        "and summarize:\n1. What kind of posts perform best\n2. Caption tone style\n3. Hashtag strategy\n"
        "4. Optimal posting time\n5. Recommendations for Swasth.AI next week.\n\n"
        f"Competitor data: {MOCK_COMPETITORS}"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert social media strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=350,
            temperature=0.6
        )
        summary = completion.choices[0].message.content.strip()
    except Exception as e:
        summary = (
            "Competitors focus on motivational, short, and emotional captions. "
            "They post morning workout and diet content around 7–9 AM. "
            "For Swasth.AI: create more 'morning routine' and 'progress transformation' content "
            "with clean visuals and consistency."
        )

    db.close()
    print("✅ Competitor analysis completed.")
    return {"summary": summary, "competitors": MOCK_COMPETITORS, "timestamp": datetime.now().isoformat()}
