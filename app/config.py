import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")

settings = Settings()