from fastapi import FastAPI
from app.routes import plan, user, analytics
from app.core.database import Base, engine

app = FastAPI(title="Swasth.AI Backend Phase 5 – Analytics Engine")

Base.metadata.create_all(bind=engine)
app.include_router(plan.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Swasth.AI v5", "message": "Analytics & Dashboard API active"}
