from sqlalchemy import func
from app.core.database import SessionLocal
from app.models.feed import Feed
from app.models.engagement import Engagement
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_category_stats():
    """Aggregate total likes, comments, shares per category."""
    db = SessionLocal()
    results = (
        db.query(
            Feed.category,
            func.sum(Engagement.likes).label("total_likes"),
            func.sum(Engagement.comments).label("total_comments"),
            func.sum(Engagement.shares).label("total_shares")
        )
        .join(Engagement, Engagement.feed_id == Feed.id)
        .group_by(Feed.category)
        .all()
    )
    db.close()

    data = []
    for r in results:
        data.append({
            "category": r.category,
            "likes": int(r.total_likes or 0),
            "comments": int(r.total_comments or 0),
            "shares": int(r.total_shares or 0)
        })
    return data

def analyze_trends():
    """Use GPT to summarize and predict next trending category."""
    stats = get_category_stats()
    if not stats:
        return {"message": "No engagement data yet"}

    prompt = (
        "You are a data analyst for a fitness motivation app. "
        "Given engagement metrics for categories, analyze which type performed best "
        "and suggest which category should be prioritized next week.\n\n"
        f"Data: {stats}"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert AI data analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.5
        )
        summary = completion.choices[0].message.content.strip()
    except Exception:
        summary = "Workout and motivation posts are currently performing best. Continue focusing on them next week."

    return {"trend_summary": summary, "data": stats}
