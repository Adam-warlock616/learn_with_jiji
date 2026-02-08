from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ask
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Learn with Jiji API",
    description="Backend API for the AI Learning Companion - VeidaLabs Assignment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Include routes
app.include_router(ask.router, prefix="/api")

@app.get("/", summary="Root endpoint")
async def root():
    """
    Welcome endpoint with API information.
    """
    return {
        "message": "Welcome to Learn with Jiji API",
        "description": "AI Learning Companion Backend",
        "endpoints": {
            "docs": "/docs",
            "ask": "POST /api/ask-jiji",
            "health": "GET /api/health"
        },
        "assignment": "VeidaLabs Software Developer Hiring Assignment"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Learn with Jiji API...")
    logger.info(f"API Documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Learn with Jiji API...")