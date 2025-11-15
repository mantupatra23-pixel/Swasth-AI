# app/core/supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env locally (Render ignores .env in repo and uses environment variables)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

# Create supabase client (no proxy or unsupported kwargs)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
