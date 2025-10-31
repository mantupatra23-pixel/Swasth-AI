from celery.schedules import crontab

# 🔹 Celery Beat Schedule Configuration
beat_schedule = {
    # 🧠 Phase 15 — Auto Social Post Scheduler (Daily Post 8AM)
    "post-daily-feed": {
        "task": "post_daily_feed",
        "schedule": crontab(hour=8, minute=0),
    },

    # 🧩 Phase 16 — Engagement Tracker (Every 3 hours)
    "track-engagement": {
        "task": "track_engagement",
        "schedule": crontab(hour="*/3", minute=0),
    },

    # 📊 Phase 17 — Weekly AI Trend Report (Every Sunday 9AM)
    "weekly-trend-report": {
        "task": "analyze_trends",
        "schedule": crontab(hour=9, minute=0, day_of_week="sun"),
    },

    # 📅 Phase 18 — Weekly AI Content Planner (Every Monday 6AM)
    "generate-weekly-plan": {
        "task": "generate_weekly_plan",
        "schedule": crontab(hour=6, minute=0, day_of_week="mon"),
    },

    # 🤖 Phase 19 — Auto Post From Planner (Daily 7AM)
    "auto-post-planner": {
        "task": "auto_post_from_planner",
        "schedule": crontab(hour=7, minute=0),
    },

    # ✍️ Phase 20 — Auto Caption Optimizer (Every night 12AM)
    "auto-optimize-captions": {
        "task": "auto_optimize_captions",
        "schedule": crontab(hour=0, minute=0),
    },

    # 🧩 Phase 21 — Hashtag Analyzer (Every night 1AM)
    "auto-analyze-hashtags": {
        "task": "auto_analyze_hashtags",
        "schedule": crontab(hour=1, minute=0),
    },
}

# 🔹 Timezone Setting
timezone = "Asia/Kolkata"

# 🔹 Broker/Backend Configuration (same for all Celery workers)
broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/0"

# 🔹 Optional Worker Settings
worker_max_tasks_per_child = 10
worker_prefetch_multiplier = 1
task_acks_late = True

"check-reminders": {
    "task": "app.services.reminder_service.run_reminders",
    "schedule": 60.0  # check every 1 minute
}
