"""
World Atlas Backend Application

FastAPI application for the World Atlas cartography platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import worlds, locations, manuscripts, characters, timeline, export
from app.database import engine, Base


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="World Atlas API",
        description="AI-powered cartography platform for writers",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS middleware for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(worlds.router, prefix="/api/v1/worlds", tags=["worlds"])
    app.include_router(locations.router, prefix="/api/v1/locations", tags=["locations"])
    app.include_router(manuscripts.router, prefix="/api/v1/manuscripts", tags=["manuscripts"])
    app.include_router(characters.router, prefix="/api/v1/characters", tags=["characters"])
    app.include_router(timeline.router, prefix="/api/v1/timeline", tags=["timeline"])
    app.include_router(export.router, prefix="/api/v1/export", tags=["export"])
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize database tables on startup (for development)."""
        if settings.ENVIRONMENT == "development":
            Base.metadata.create_all(bind=engine)
    
    return app


app = create_application()
