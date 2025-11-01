from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# ✅ Fix: use pg8000 driver for compatibility
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://")

# ✅ Clean correct syntax
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
