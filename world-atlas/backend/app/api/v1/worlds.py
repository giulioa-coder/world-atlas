"""
Worlds API router.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.world_service import WorldService
from app.schemas.world import WorldCreate, WorldUpdate, WorldResponse, WorldListResponse
from app.core.exceptions import NotFoundException


router = APIRouter()


def get_world_service(db: Session = Depends(get_db)) -> WorldService:
    """Dependency for WorldService."""
    return WorldService(db)


@router.post("/worlds/", response_model=WorldResponse, status_code=201)
def create_world(
    schema: WorldCreate,
    service: WorldService = Depends(get_world_service),
):
    """Create a new world."""
    return service.create(schema)


@router.get("/worlds/", response_model=WorldListResponse)
def list_worlds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: WorldService = Depends(get_world_service),
):
    """List all worlds."""
    worlds = service.list(skip=skip, limit=limit)
    total = service.count()
    return WorldListResponse(items=[WorldResponse.model_validate(w) for w in worlds], total=total)


@router.get("/worlds/search", response_model=WorldListResponse)
def search_worlds(
    q: str = Query(..., min_length=1, description="Search query for world name/description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: WorldService = Depends(get_world_service),
):
    """Search worlds by name or description (case-insensitive)."""
    worlds = service.search(q, skip=skip, limit=limit)
    total = service.count_search(q)
    return WorldListResponse(items=[WorldResponse.model_validate(w) for w in worlds], total=total)


@router.get("/worlds/{world_id}", response_model=WorldResponse)
def get_world(
    world_id: UUID,
    service: WorldService = Depends(get_world_service),
):
    """Get a specific world by ID."""
    world = service.get(world_id)
    if not world:
        raise NotFoundException("World", world_id)
    return WorldResponse.model_validate(world)


@router.put("/worlds/{world_id}", response_model=WorldResponse)
def update_world(
    world_id: UUID,
    schema: WorldUpdate,
    service: WorldService = Depends(get_world_service),
):
    """Update an existing world."""
    world = service.update(world_id, schema)
    if not world:
        raise NotFoundException("World", world_id)
    return WorldResponse.model_validate(world)


@router.delete("/worlds/{world_id}", status_code=204)
def delete_world(
    world_id: UUID,
    service: WorldService = Depends(get_world_service),
):
    """Delete a world."""
    success = service.delete(world_id)
    if not success:
        raise NotFoundException("World", world_id)
    return None
