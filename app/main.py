from fastapi import FastAPI
from app.routes import plan, user, analytics
from app.core.database import Base, engine
from app.routes import admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Initialize FastAPI app
app = FastAPI(title="Swasth.AI Backend Phase 5 – Analytics Engine")

# Create all database tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(plan.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

# Root endpoint
@app.get("/")
def root():
    return {
        "status": "Swasth.AI v5",
        "message": "Analytics & Dashboard API is running successfully 🚀"
    }

# ---------------------------------------
# ✅ Security Configurations
# ---------------------------------------

# CORS settings
origins = [
    "http://localhost:3000",
    "https://swasth.ai",
    "https://swasthai.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["swasth.ai", "*.swasth.ai", "localhost"]
)
