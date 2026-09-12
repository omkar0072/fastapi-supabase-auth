import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_JWT_SECRET:
    raise ValueError(
        "Missing required environment variables. "
        "Please check your .env file against .env.example."
    )
