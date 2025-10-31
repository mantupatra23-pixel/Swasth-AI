import requests, os
from app.core.database import SessionLocal
from app.models.engagement import Engagement
from app.models.feed import Feed
from dotenv import load_dotenv
load_dotenv()

IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_PAGE_ID = os.getenv("IG_PAGE_ID")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def fetch_instagram_metrics(post_id):
    """Fetch likes/comments for Instagram post"""
    try:
        url = f"https://graph.facebook.com/v18.0/{post_id}?fields=like_count,comments_count&access_token={IG_ACCESS_TOKEN}"
        res = requests.get(url).json()
        return {
            "likes": res.get("like_count", 0),
            "comments": res.get("comments_count", 0),
            "shares": 0
        }
    except Exception as e:
        print(f"⚠️ IG fetch failed: {e}")
        return {"likes": 0, "comments": 0, "shares": 0}

def fetch_twitter_metrics(tweet_id):
    """Fetch metrics for Twitter post"""
    try:
        headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
        url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=public_metrics"
        res = requests.get(url, headers=headers).json()
        data = res.get("data", {}).get("public_metrics", {})
        return {
            "likes": data.get("like_count", 0),
            "comments": data.get("reply_count", 0),
            "shares": data.get("retweet_count", 0)
        }
    except Exception as e:
        print(f"⚠️ Twitter fetch failed: {e}")
        return {"likes": 0, "comments": 0, "shares": 0}

def update_engagement(feed_id: int, platform: str, post_id: str):
    db = SessionLocal()
    metrics = {}
    if platform == "instagram":
        metrics = fetch_instagram_metrics(post_id)
    elif platform == "twitter":
        metrics = fetch_twitter_metrics(post_id)

    existing = (
        db.query(Engagement)
        .filter(Engagement.feed_id == feed_id, Engagement.platform == platform)
        .first()
    )

    if existing:
        existing.likes = metrics["likes"]
        existing.comments = metrics["comments"]
        existing.shares = metrics["shares"]
    else:
        new = Engagement(feed_id=feed_id, platform=platform, post_id=post_id, **metrics)
        db.add(new)

    db.commit()
    db.close()
    print(f"✅ Updated {platform} metrics for feed {feed_id}: {metrics}")
