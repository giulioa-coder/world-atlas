"""
Location Service - Business logic for managing locations.

Handles CRUD operations, coordinate validation, and status management.
"""

from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.location import Location, LocationType, LocationStatus, LocationMention
from app.models.world import World
from app.schemas.location import LocationCreate, LocationUpdate, LocationMentionCreate


class LocationService:
    """Service for managing locations in the world model."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_location(self, location_id: UUID) -> Optional[Location]:
        """Get a single location by ID."""
        result = await self.db.execute(
            select(Location)
            .options(selectinload(Location.mentions))
            .where(Location.id == location_id)
        )
        return result.scalar_one_or_none()
    
    async def get_locations_by_world(self, world_id: UUID) -> List[Location]:
        """Get all locations for a world."""
        result = await self.db.execute(
            select(Location)
            .options(selectinload(Location.mentions))
            .where(Location.world_id == world_id)
            .order_by(Location.name)
        )
        return list(result.scalars().all())
    
    async def get_locations_by_type(
        self, 
        world_id: UUID, 
        location_type: LocationType
    ) -> List[Location]:
        """Get locations of a specific type in a world."""
        result = await self.db.execute(
            select(Location)
            .where(Location.world_id == world_id)
            .where(Location.location_type == location_type)
            .order_by(Location.name)
        )
        return list(result.scalars().all())
    
    async def create_location(self, data: LocationCreate) -> Location:
        """Create a new location."""
        location = Location(
            world_id=data.world_id,
            name=data.name,
            location_type=data.location_type,
            latitude=data.latitude,
            longitude=data.longitude,
            elevation=data.elevation,
            description=data.description,
            visual_description=data.visual_description,
            importance=data.importance or 1,
            confidence=data.confidence or 0.5,
            status=data.status or LocationStatus.CANONICAL,
            metadata=data.metadata or {},
        )
        
        self.db.add(location)
        await self.db.flush()
        await self.db.refresh(location)
        
        # Add initial mention if provided
        if data.initial_mention:
            mention = LocationMention(
                location_id=location.id,
                chapter_id=data.initial_mention.chapter_id,
                text_span=data.initial_mention.text_span,
                context=data.initial_mention.context,
                confidence=data.initial_mention.confidence or 0.9,
                extraction_method="manual",
            )
            self.db.add(mention)
            await self.db.flush()
        
        return location
    
    async def update_location(
        self, 
        location_id: UUID, 
        data: LocationUpdate
    ) -> Optional[Location]:
        """Update an existing location."""
        location = await self.get_location(location_id)
        if not location:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(location, field, value)
        
        location.updated_at = datetime.utcnow()
        
        await self.db.flush()
        await self.db.refresh(location)
        
        return location
    
    async def update_location_coordinates(
        self,
        location_id: UUID,
        latitude: float,
        longitude: float
    ) -> Optional[Location]:
        """Update only the coordinates of a location."""
        return await self.update_location(
            location_id,
            LocationUpdate(latitude=latitude, longitude=longitude)
        )
    
    async def promote_to_canonical(self, location_id: UUID) -> Optional[Location]:
        """Promote a location to canonical status."""
        return await self.update_location(
            location_id,
            LocationUpdate(status=LocationStatus.CANONICAL)
        )
    
    async def reject_location(self, location_id: UUID) -> Optional[Location]:
        """Mark a location as rejected."""
        return await self.update_location(
            location_id,
            LocationUpdate(status=LocationStatus.REJECTED)
        )
    
    async def delete_location(self, location_id: UUID) -> bool:
        """Delete a location."""
        location = await self.get_location(location_id)
        if not location:
            return False
        
        await self.db.delete(location)
        await self.db.flush()
        return True
    
    async def add_mention(
        self, 
        location_id: UUID, 
        data: LocationMentionCreate
    ) -> LocationMention:
        """Add a mention evidence to a location."""
        mention = LocationMention(
            location_id=location_id,
            chapter_id=data.chapter_id,
            text_span=data.text_span,
            context=data.context,
            paragraph_index=data.paragraph_index,
            sentence_index=data.sentence_index,
            confidence=data.confidence or 0.5,
            extraction_method=data.extraction_method or "manual",
        )
        
        self.db.add(mention)
        await self.db.flush()
        await self.db.refresh(mention)
        
        return mention
    
    async def get_mentions_by_location(self, location_id: UUID) -> List[LocationMention]:
        """Get all mentions for a location."""
        result = await self.db.execute(
            select(LocationMention)
            .where(LocationMention.location_id == location_id)
            .order_by(LocationMention.created_at)
        )
        return list(result.scalars().all())
    
    async def search_locations(
        self,
        world_id: UUID,
        query: str,
        limit: int = 20
    ) -> List[Location]:
        """Search locations by name or description."""
        search_pattern = f"%{query}%"
        result = await self.db.execute(
            select(Location)
            .where(Location.world_id == world_id)
            .where(
                (Location.name.ilike(search_pattern)) |
                (Location.description.ilike(search_pattern))
            )
            .limit(limit)
        )
        return list(result.scalars().all())
