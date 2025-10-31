from openai import OpenAI
from app.core.database import SessionLocal
from app.models.content_plan import ContentPlan
import os, random
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_hashtags(plan_id: int):
    """AI-powered trending hashtag analyzer for optimized captions."""
    db = SessionLocal()
    plan = db.query(ContentPlan).filter(ContentPlan.id == plan_id).first()
    if not plan:
        return {"error": "Plan not found"}

    base_caption = plan.optimized_caption or plan.caption
    category = plan.category

    prompt = (
        f"You are a social media trend expert. Analyze current Instagram and Twitter trends in {category} niche. "
        f"Suggest 8–10 hashtags that are most relevant to this caption: '{base_caption}'. "
        "For each hashtag, predict a popularity score (1–100) based on current fitness and motivation trends. "
        "Return JSON array like [{'hashtag': '#example', 'score': 85}]."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in Instagram trend analytics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.6
        )
        result = completion.choices[0].message.content.strip()
    except Exception:
        result = """[
          {"hashtag": "#MotivationMonday", "score": 92},
          {"hashtag": "#FitnessGoals", "score": 88},
          {"hashtag": "#SwasthAI", "score": 85},
          {"hashtag": "#Workout", "score": 81},
          {"hashtag": "#SelfImprovement", "score": 77}
        ]"""

    # Clean result
    import json
    try:
        hashtags_data = json.loads(result)
    except Exception:
        hashtags_data = [
            {"hashtag": "#SwasthAI", "score": 80},
            {"hashtag": "#HealthFirst", "score": 76}
        ]

    # Combine top hashtags into string
    top_hashtags = " ".join([h["hashtag"] for h in hashtags_data])
    avg_score = sum([h["score"] for h in hashtags_data]) / len(hashtags_data)

    plan.hashtags = top_hashtags
    plan.hashtag_score = round(avg_score, 2)
    db.commit()
    db.close()

    print(f"✅ Hashtags updated for plan {plan_id}: {top_hashtags}")
    return {"plan_id": plan_id, "hashtags": hashtags_data, "average_score": avg_score}
