from .plan import router as plan
from .user import router as user
from .analytics import router as analytics
from .subscription import router as subscription
routers = [plan, user, analytics, subscription]

routers = [plan, user, analytics]
