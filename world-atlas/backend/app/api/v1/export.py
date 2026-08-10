"""
Export API router - stub implementation for Phase 1.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter()


@router.get("/worlds/{world_id}/png")
def export_png(
    world_id: UUID,
    width: int = Query(1920, ge=800, le=4096),
    height: int = Query(1080, ge=600, le=2160),
    db: Session = Depends(get_db),
):
    """
    Export map as PNG image.
    
    TODO: Implement full export functionality in Phase 9.
    Currently returns a stub response.
    """
    return {
        "message": "PNG export endpoint",
        "world_id": str(world_id),
        "dimensions": {"width": width, "height": height},
        "note": "Full export functionality will be implemented in Phase 9"
    }


@router.get("/worlds/{world_id}/svg")
def export_svg(
    world_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Export map as SVG vector image.
    
    TODO: Implement full export functionality in Phase 9.
    Currently returns a stub response.
    """
    return {
        "message": "SVG export endpoint",
        "world_id": str(world_id),
        "note": "Full export functionality will be implemented in Phase 9"
    }


@router.get("/worlds/{world_id}/pdf")
def export_pdf(
    world_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Export map as PDF document.
    
    TODO: Implement full export functionality in Phase 9.
    Currently returns a stub response.
    """
    return {
        "message": "PDF export endpoint",
        "world_id": str(world_id),
        "note": "Full export functionality will be implemented in Phase 9"
    }
