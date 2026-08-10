"""
Timeline API router - stub implementation for Phase 1.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter()


@router.get("/worlds/{world_id}/")
def get_timeline(
    world_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get character journey timeline for a world.
    
    TODO: Implement full timeline functionality in Phase 5.
    Currently returns a stub response.
    """
    return {
        "message": "Timeline endpoint",
        "world_id": str(world_id),
        "note": "Full timeline functionality will be implemented in Phase 5",
        "journeys": []
    }
