"""
Locations API router.

Handles CRUD operations for locations and mentions.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.world import World
from app.models.location import Location, LocationStatus
from app.schemas.location import (
    LocationCreate, LocationUpdate, LocationResponse, 
    LocationListResponse, LocationMentionCreate, LocationMentionResponse
)
from app.core.exceptions import NotFoundException
from app.services.location_service import LocationService


router = APIRouter()


def get_location_service(db: Session = Depends(get_db)) -> LocationService:
    """Dependency for location service."""
    return LocationService(db)


@router.post("/worlds/{world_id}/", response_model=LocationResponse, status_code=201)
async def create_location(
    world_id: UUID,
    schema: LocationCreate,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Create a new location in a world."""
    # Verify world exists
    world = db.get(World, world_id)
    if not world:
        raise NotFoundException("World", world_id)
    
    location = service.create_location(world_id, schema)
    db.commit()
    db.refresh(location)
    return LocationResponse.model_validate(location)


@router.get("/worlds/{world_id}/", response_model=LocationListResponse)
async def list_locations(
    world_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    location_type: Optional[str] = None,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """List all locations in a world."""
    if location_type:
        from app.models.location import LocationType
        try:
            loc_type = LocationType(location_type)
            locations = service.get_locations_by_type(world_id, loc_type)
        except ValueError:
            locations = service.get_locations_by_world(world_id)
    else:
        locations = service.get_locations_by_world(world_id)
    
    # Apply pagination manually since service returns all
    paginated = locations[skip:skip+limit]
    
    return LocationListResponse(
        items=[LocationResponse.model_validate(loc) for loc in paginated],
        total=len(locations)
    )


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Get a specific location by ID."""
    location = service.get_location(location_id)
    if not location:
        raise NotFoundException("Location", location_id)
    return LocationResponse.model_validate(location)


@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: UUID,
    schema: LocationUpdate,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Update an existing location."""
    location = service.update_location(location_id, schema)
    if not location:
        raise NotFoundException("Location", location_id)
    db.commit()
    db.refresh(location)
    return LocationResponse.model_validate(location)


@router.patch("/{location_id}/coordinates", response_model=LocationResponse)
async def update_location_coordinates(
    location_id: UUID,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Update only the coordinates of a location (for map editor)."""
    location = service.update_location_coordinates(location_id, latitude, longitude)
    if not location:
        raise NotFoundException("Location", location_id)
    db.commit()
    db.refresh(location)
    return LocationResponse.model_validate(location)


@router.post("/{location_id}/promote", response_model=LocationResponse)
async def promote_to_canonical(
    location_id: UUID,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Promote a location to canonical status."""
    location = service.promote_to_canonical(location_id)
    if not location:
        raise NotFoundException("Location", location_id)
    db.commit()
    db.refresh(location)
    return LocationResponse.model_validate(location)


@router.post("/{location_id}/reject", response_model=LocationResponse)
async def reject_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Mark a location as rejected."""
    location = service.reject_location(location_id)
    if not location:
        raise NotFoundException("Location", location_id)
    db.commit()
    db.refresh(location)
    return LocationResponse.model_validate(location)


@router.delete("/{location_id}", status_code=204)
async def delete_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Delete a location."""
    success = service.delete_location(location_id)
    if not success:
        raise NotFoundException("Location", location_id)
    return None


# Mention endpoints for evidence tracking


@router.post("/{location_id}/mentions", response_model=LocationMentionResponse, status_code=201)
async def add_location_mention(
    location_id: UUID,
    schema: LocationMentionCreate,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Add a mention evidence to a location."""
    # Verify location exists
    location = service.get_location(location_id)
    if not location:
        raise NotFoundException("Location", location_id)
    
    mention = service.add_mention(location_id, schema)
    db.commit()
    db.refresh(mention)
    return LocationMentionResponse.model_validate(mention)


@router.get("/{location_id}/mentions", response_model=List[LocationMentionResponse])
async def get_location_mentions(
    location_id: UUID,
    db: Session = Depends(get_db),
    service: LocationService = Depends(get_location_service),
):
    """Get all mentions for a location."""
    location = service.get_location(location_id)
    if not location:
        raise NotFoundException("Location", location_id)
    
    mentions = service.get_mentions_by_location(location_id)
    return [LocationMentionResponse.model_validate(m) for m in mentions]
