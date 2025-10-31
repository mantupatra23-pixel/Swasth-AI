import requests, os, time
import tweepy
from dotenv import load_dotenv
load_dotenv()

# Instagram Post
def post_to_instagram(image_url: str, caption: str):
    page_id = os.getenv("IG_PAGE_ID")
    access_token = os.getenv("IG_ACCESS_TOKEN")

    try:
        # Step 1: Create container
        create_url = f"https://graph.facebook.com/v18.0/{page_id}/media"
        payload = {"image_url": image_url, "caption": caption, "access_token": access_token}
        res = requests.post(create_url, data=payload).json()
        container_id = res.get("id")

        # Step 2: Publish post
        publish_url = f"https://graph.facebook.com/v18.0/{page_id}/media_publish"
        publish = requests.post(publish_url, data={"creation_id": container_id, "access_token": access_token}).json()
        print(f"✅ Instagram Post Success: {publish}")
        return publish
    except Exception as e:
        print(f"⚠️ Instagram Post Failed: {e}")
        return None

# Twitter Post
def post_to_twitter(image_url: str, caption: str):
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        tweet_text = f"{caption}\n\n{image_url}"
        tweet = client.create_tweet(text=tweet_text)
        print(f"✅ Tweeted: {tweet.data}")
        return tweet.data
    except Exception as e:
        print(f"⚠️ Twitter Post Failed: {e}")
        return None
