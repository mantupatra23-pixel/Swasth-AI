# app/core/supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load local .env if present (useful for local dev). On Render the env vars come from the environment.
load_dotenv()

def get_supabase_client() -> Client:
    """
    Initialize and return a Supabase client.
    Expects SUPABASE_URL and SUPABASE_KEY to be available as environment variables.
    """

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        # Clear, actionable error if variables are missing
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    # Create and return the client WITHOUT proxy/http_client/client_options arguments
    supabase: Client = create_client(url, key)
    return supabase
