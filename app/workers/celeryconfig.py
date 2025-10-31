from celery.schedules import crontab
from celery.schedules import crontab

beat_schedule = {
    "generate-daily-feed": {
        "task": "generate_daily_feed",
        "schedule": crontab(hour=7, minute=0),
    },
    "post-daily-feed": {
        "task": "post_daily_feed",
        "schedule": crontab(hour=8, minute=0),  # post 1 hour later
    }
}
timezone = "Asia/Kolkata"

beat_schedule = {
    "generate-daily-feed": {
        "task": "generate_daily_feed",
        "schedule": crontab(hour=7, minute=0),  # Every day at 7 AM
    }
}
timezone = "Asia/Kolkata"

"track-engagement": {
        "task": "track_engagement",
        "schedule": crontab(hour="*/3", minute=0),  # every 3 hours
    }
