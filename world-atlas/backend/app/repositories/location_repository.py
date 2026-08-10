"""
Location repository for database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.location import Location, LocationType, LocationStatus
from app.repositories.base import Repository


class LocationRepository(Repository[Location]):
    """Repository for Location model operations."""
    
    def __init__(self, db: Session):
        super().__init__(model=Location, db=db)
    
    def get_by_world(self, world_id: UUID) -> List[Location]:
        """Get all locations for a specific world."""
        return self.db.query(Location).filter(Location.world_id == world_id).all()
    
    def get_by_type(self, location_type: LocationType) -> List[Location]:
        """Get locations by type."""
        return self.db.query(Location).filter(Location.location_type == location_type).all()
    
    def get_by_status(self, status: LocationStatus) -> List[Location]:
        """Get locations by status."""
        return self.db.query(Location).filter(Location.status == status).all()
    
    def get_by_world_and_type(
        self, 
        world_id: UUID, 
        location_type: LocationType
    ) -> List[Location]:
        """Get locations for a specific world and type."""
        return self.db.query(Location).filter(
            Location.world_id == world_id,
            Location.location_type == location_type
        ).all()
    
    def search_by_name(self, world_id: UUID, search_term: str) -> List[Location]:
        """Search locations by name within a world."""
        search_pattern = f"%{search_term}%"
        return self.db.query(Location).filter(
            Location.world_id == world_id,
            Location.name.ilike(search_pattern)
        ).all()
    
    def get_with_coordinates(self, world_id: UUID) -> List[Location]:
        """Get locations that have coordinates."""
        return self.db.query(Location).filter(
            Location.world_id == world_id,
            Location.latitude.isnot(None),
            Location.longitude.isnot(None)
        ).all()
    
    def update_position(
        self, 
        id: UUID, 
        latitude: float, 
        longitude: float
    ) -> Optional[Location]:
        """Update location coordinates."""
        return self.update(id, latitude=latitude, longitude=longitude)
    
    def get_by_importance(
        self, 
        world_id: UUID, 
        min_importance: int = 3
    ) -> List[Location]:
        """Get locations with importance above threshold."""
        return self.db.query(Location).filter(
            Location.world_id == world_id,
            Location.importance >= min_importance
        ).all()
