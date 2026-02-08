from fastapi import HTTPException, Header
from typing import Optional

async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Mock auth middleware - in production, validate JWT with Supabase Auth
    """
    if not authorization:
        # For demo, allow anonymous queries
        return None
    
    # In real app: validate JWT token with Supabase
    # token = authorization.replace("Bearer ", "")
    # user = supabase.auth.get_user(token)
    
    # Mock: return user_id from header
    return "demo-user-id"