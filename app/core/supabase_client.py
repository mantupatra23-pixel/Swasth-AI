# app/core/supabase_client.py
import os
import traceback
from supabase import create_client
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

_supabase = None

def _try_create(url: str, key: str):
    """
    Try to call create_client, but catch TypeError coming from an incompatible
    supabase/httpx client signature and raise clearer error.
    """
    try:
        return create_client(url, key)
    except TypeError as e:
        # capture stack for logs
        tb = traceback.format_exc()
        # re-raise a clearer error message for Render logs
        raise RuntimeError(
            "Failed to initialize Supabase client due to incompatible client signature.\n"
            "Original TypeError: " + str(e) + "\n\n"
            "Traceback:\n" + tb + "\n\n"
            "Likely cause: installed 'supabase' package version is incompatible with the code.\n"
            "Fix: pin a compatible supabase package version in requirements.txt (see instructions).\n"
        ) from e
    except Exception:
        # propagate other errors
        raise

def get_supabase_client():
    global _supabase
    if _supabase is not None:
        return _supabase

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    _supabase = _try_create(url, key)
    return _supabase

# Export a variable (may be None until get_supabase_client is called)
supabase = None
try:
    supabase = _try_create(os.getenv("SUPABASE_URL") or "", os.getenv("SUPABASE_KEY") or "")
except Exception:
    # ignore here so import doesn't crash — app will get explicit error when calling get_supabase_client()
    supabase = None

__all__ = ["supabase", "get_supabase_client"]
