from supabase.client import create_client, Client
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SupabaseClient:
    # Remove type annotation from class variable
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance.client = None  # Will be set in initialize
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        try:
            # Get values - add checks
            url = settings.SUPABASE_URL
            key = settings.SUPABASE_KEY
            
            if url is None or key is None:
                raise ValueError("SUPABASE_URL or SUPABASE_KEY is not set in .env file")
            
            self.client = create_client(url, key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    
    def get_client(self) -> Client:
        if self.client is None:
            raise RuntimeError("Supabase client not initialized")
        return self.client

# Global instance
supabase = SupabaseClient()