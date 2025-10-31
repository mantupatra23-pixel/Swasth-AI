from fastapi import FastAPI
from app.routes import plan, user
from app.core.database import Base, engine

app = FastAPI(title="Swasth.AI Backend Phase 2")

Base.metadata.create_all(bind=engine)

# include routers
app.include_router(plan.router, prefix="/api")
app.include_router(user.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Swasth.AI Backend v2", "message": "User + History system active"}
