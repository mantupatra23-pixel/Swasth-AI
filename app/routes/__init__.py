from .plan import router as plan
from .user import router as user
from .analytics import router as analytics
from .subscription import router as subscription
from .ai_chat import router as ai_chat
from .voice import router as voice
from .feed import router as feed
from .share import router as share
from .trends import router as trends
from .planner import router as planner
from .caption import router as caption
from .hashtag import router as hashtag
from .competitor import router as competitor
from .health_user import router as health_user
from .workout import router as workout
from .diet import router as diet
from .progress import router as progress
from .health import router as health
from .coach import router as coach
from .reminder import router as reminder
from .community import router as community
from .voice import router as voice

routers = [plan, user, health_user, workout, diet, progress, health, coach, reminder, community, voice]
routers = [plan, user, health_user, workout, diet, progress, health, coach, reminder, community]
routers = [plan, user, health_user, workout, diet, progress, health, coach, reminder]
routers = [plan, user, health_user, workout, diet, progress, health, coach]
routers = [plan, user, health_user, workout, diet, progress, health]
routers = [plan, user, health_user, workout, diet, progress]
routers = [plan, user, health_user, workout, diet]
routers = [plan, user, health_user, workout]
routers = [plan, user, health_user]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share, engagement, trends, planner, caption, hashtag, competitor]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share, engagement, trends, planner, caption, hashtag]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share, engagement, trends, planner, caption]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share, engagement, trends, planner]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share, engagement, trends]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice]
routers = [plan, user, analytics, subscription, admin, ai_chat]
routers = [plan, user, analytics, subscription]
routers = [plan, user, analytics]
