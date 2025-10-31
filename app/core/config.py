import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/swasthai")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
