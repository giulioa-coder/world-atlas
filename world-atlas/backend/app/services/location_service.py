"""
Location Service - Business logic for managing locations.

Handles CRUD operations, coordinate validation, and status management.
"""

from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.location import Location, LocationType, LocationStatus, LocationMention
from app.models.world import World
from app.schemas.location import LocationCreate, LocationUpdate, LocationMentionCreate
from app.repositories.location_repository import LocationRepository


class LocationService:
    """Service for managing locations in the world model."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = LocationRepository(db)
    
    def get_location(self, location_id: UUID) -> Optional[Location]:
        """Get a single location by ID."""
        result = self.db.execute(
            select(Location)
            .options(selectinload(Location.mentions))
            .where(Location.id == location_id)
        )
        return result.scalar_one_or_none()
    
    def get_locations_by_world(self, world_id: UUID) -> List[Location]:
        """Get all locations for a world."""
        return self.repository.get_by_world(world_id)
    
    def get_locations_by_type(
        self, 
        world_id: UUID, 
        location_type: LocationType
    ) -> List[Location]:
        """Get locations of a specific type in a world."""
        return self.repository.get_by_world_and_type(world_id, location_type)
    
    def create_location(self, world_id: UUID, data: LocationCreate) -> Location:
        """Create a new location."""
        location = Location(
            world_id=world_id,
            name=data.name,
            location_type=data.location_type,
            latitude=data.latitude,
            longitude=data.longitude,
            elevation=data.elevation,
            description=data.description,
            visual_description=data.visual_description,
            importance=data.importance or 1,
            confidence=0.5,
            status=LocationStatus.CANONICAL,
            extra_data=data.extra_data or {},
        )
        
        self.db.add(location)
        self.db.flush()
        self.db.refresh(location)
        
        # Add initial mention if provided
        if hasattr(data, 'initial_mention') and data.initial_mention:
            mention = LocationMention(
                location_id=location.id,
                chapter_id=data.initial_mention.chapter_id,
                text_span=data.initial_mention.text_span,
                context=data.initial_mention.context,
                confidence=data.initial_mention.confidence or 0.9,
                extraction_method="manual",
            )
            self.db.add(mention)
            self.db.flush()
        
        return location
    
    def update_location(
        self, 
        location_id: UUID, 
        data: LocationUpdate
    ) -> Optional[Location]:
        """Update an existing location."""
        location = self.get_location(location_id)
        if not location:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(location, field, value)
        
        location.updated_at = datetime.utcnow()
        
        self.db.flush()
        self.db.refresh(location)
        
        return location
    
    def update_location_coordinates(
        self,
        location_id: UUID,
        latitude: float,
        longitude: float,
    ) -> Optional[Location]:
        """Update only coordinates of a location."""
        return self.repository.update_position(location_id, latitude, longitude)
    
    def promote_to_canonical(self, location_id: UUID) -> Optional[Location]:
        """Promote a location to canonical status."""
        location = self.get_location(location_id)
        if not location:
            return None
        
        location.status = LocationStatus.CANONICAL
        location.confidence = 1.0
        
        self.db.flush()
        self.db.refresh(location)
        
        return location
    
    def reject_location(self, location_id: UUID) -> Optional[Location]:
        """Mark a location as rejected."""
        location = self.get_location(location_id)
        if not location:
            return None
        
        location.status = LocationStatus.REJECTED
        location.confidence = 0.0
        
        self.db.flush()
        self.db.refresh(location)
        
        return location
    
    def delete_location(self, location_id: UUID) -> bool:
        """Delete a location."""
        return self.repository.delete(location_id)
    
    def add_mention(
        self, 
        location_id: UUID, 
        data: LocationMentionCreate
    ) -> LocationMention:
        """Add a mention to a location."""
        mention = LocationMention(
            location_id=location_id,
            chapter_id=data.chapter_id,
            text_span=data.text_span,
            context=data.context,
            paragraph_index=data.paragraph_index,
            sentence_index=data.sentence_index,
            confidence=data.confidence,
            extraction_method=data.extraction_method,
        )
        
        self.db.add(mention)
        self.db.flush()
        self.db.refresh(mention)
        
        return mention
    
    def get_mentions_by_location(self, location_id: UUID) -> List[LocationMention]:
        """Get all mentions for a location."""
        result = self.db.execute(
            select(LocationMention)
            .where(LocationMention.location_id == location_id)
            .order_by(LocationMention.created_at)
        )
        return list(result.scalars().all())
    
    def search_locations(self, world_id: UUID, query: str, skip: int = 0, limit: int = 100) -> List[Location]:
        """Search locations in a world by name or description (case-insensitive)."""
        search_pattern = f"%{query}%"
        result = self.db.execute(
            select(Location)
            .where(Location.world_id == world_id)
            .filter(
                (Location.name.ilike(search_pattern)) | 
                (Location.description.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    def count_search_locations(self, world_id: UUID, query: str) -> int:
        """Count locations matching search term in a world."""
        from sqlalchemy import func
        search_pattern = f"%{query}%"
        result = self.db.execute(
            select(func.count(Location.id))
            .where(Location.world_id == world_id)
            .filter(
                (Location.name.ilike(search_pattern)) | 
                (Location.description.ilike(search_pattern))
            )
        )
        return result.scalar_one() or 0
