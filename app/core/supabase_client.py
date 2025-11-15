# app/core/supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional

# Load .env for local dev. On Render the env vars come from the environment.
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Top-level variable so other modules can import "supabase" directly.
# We try to create the client now if vars exist; otherwise keep None and create lazily.
_supabase: Optional[Client] = None

def _create_client_if_possible() -> Optional[Client]:
    global _supabase
    if _supabase is not None:
        return _supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if url and key:
        _supabase = create_client(url, key)
        return _supabase
    return None

# attempt to create at import time only if env vars are present
_create_client_if_possible()

def get_supabase_client() -> Client:
    """
    Return a Supabase client. If it can't be created because environment variables
    are missing, raise a clear ValueError.
    """
    global _supabase
    if _supabase is not None:
        return _supabase

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    _supabase = create_client(url, key)
    return _supabase

# public name expected by other modules
supabase = _supabase

__all__ = ["supabase", "get_supabase_client"]
