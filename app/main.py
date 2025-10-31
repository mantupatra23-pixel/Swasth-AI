from fastapi import FastAPI
from app.routes import plan
from app.core.database import Base, engine

app = FastAPI(title="Swasth.AI - Plan Engine")

Base.metadata.create_all(bind=engine)
app.include_router(plan.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Swasth.AI Plan Engine running"}
