from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    query_text: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        examples=["Explain RAG"]
    )
    user_id: Optional[str] = Field(
        None,
        examples=["user-uuid-123"]
    )

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    type: str
    file_url: str
    tags: List[str]

class QueryResponse(BaseModel):
    answer: str
    resources: List[ResourceResponse]

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    supabase_connected: bool