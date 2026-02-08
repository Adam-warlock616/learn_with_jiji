from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import QueryRequest, QueryResponse, ResourceResponse
from app.utils.supabase_client import supabase
from app.utils.auth import get_current_user
import logging
from typing import List

router = APIRouter()
logger = logging.getLogger(__name__)

def search_resources(query: str) -> List[dict]:
    """
    Search resources by query text
    """
    try:
        client = supabase.get_client()
        
        # Simple search - get all and filter in Python
        response = client.table('resources').select('*').limit(20).execute()
        
        if not response.data:
            return []
        
        # Filter in Python
        query_lower = query.lower()
        results = []
        
        for resource in response.data:
            # Check title
            if query_lower in resource['title'].lower():
                results.append(resource)
                continue
            
            # Check description
            if resource.get('description') and query_lower in resource['description'].lower():
                results.append(resource)
                continue
            
            # Check tags
            tags = resource.get('tags', [])
            if tags and any(query_lower in tag.lower() for tag in tags):
                results.append(resource)
                continue
        
        # If no matches, return some resources
        if not results:
            return response.data[:3]
        
        return results[:5]
    
    except Exception as e:
        logger.error(f"Error searching resources: {e}")
        return []

def generate_answer(query: str, resources: List[dict]) -> str:
    """
    Generate a contextual answer based on found resources
    """
    if not resources:
        return f"I'm still learning about '{query}'. Please try a different topic."
    
    resource_types = {}
    for r in resources:
        resource_types.setdefault(r['type'], 0)
        resource_types[r['type']] += 1
    
    type_summary = []
    if 'ppt' in resource_types:
        type_summary.append(f"{resource_types['ppt']} presentation(s)")
    if 'video' in resource_types:
        type_summary.append(f"{resource_types['video']} video(s)")
    
    return (
        f"Here's what I found about '{query}': "
        f"I have {len(resources)} resources for you including {', '.join(type_summary)}. "
        f"Start with '{resources[0]['title']}' for a comprehensive overview."
    )

@router.post("/ask-jiji", response_model=QueryResponse, summary="Ask Jiji a question")
async def ask_jiji(
    request: QueryRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Process user query and return relevant learning resources.
    """
    try:
        # 1. Log the query (optional)
        if user_id:
            try:
                client = supabase.get_client()
                client.table('queries').insert({
                    'user_id': user_id,
                    'query_text': request.query_text
                }).execute()
            except Exception as e:
                logger.warning(f"Failed to log query: {e}")
        
        # 2. Search for relevant resources
        resources = search_resources(request.query_text.lower())
        
        # 3. Generate contextual answer
        answer = generate_answer(request.query_text, resources)
        
        # 4. Format response
        formatted_resources = []
        for r in resources:
            formatted_resources.append(
                ResourceResponse(
                    id=r['id'],
                    title=r['title'],
                    description=r['description'],
                    type=r['type'],
                    file_url=r['file_url'],
                    tags=r.get('tags', [])
                )
            )
        
        return QueryResponse(
            answer=answer,
            resources=formatted_resources
        )
        
    except Exception as e:
        logger.error(f"Error in ask-jiji endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while processing your query"
        )

@router.get("/health", summary="Health check endpoint")
async def health_check():
    """
    Check if API and Supabase are working.
    """
    try:
        client = supabase.get_client()
        # Test Supabase connection
        response = client.table('resources').select('*').limit(1).execute()
        supabase_connected = True if response.data else False
    except Exception as e:
        logger.error(f"Supabase health check failed: {e}")
        supabase_connected = False
    
    return {
        "status": "healthy" if supabase_connected else "degraded",
        "supabase_connected": supabase_connected,
        "message": "API is running" if supabase_connected else "API running but Supabase connection failed"
    }