from .plan import router as plan
from .user import router as user
from .analytics import router as analytics
from .subscription import router as subscription
from .ai_chat import router as ai_chat
from .voice import router as voice
from .feed import router as feed
from .share import router as share

routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed, share]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice, feed]
routers = [plan, user, analytics, subscription, admin, ai_chat, voice]
routers = [plan, user, analytics, subscription, admin, ai_chat]
routers = [plan, user, analytics, subscription]
routers = [plan, user, analytics]
