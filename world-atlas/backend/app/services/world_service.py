"""
World service for business logic operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.world import World
from app.schemas.world import WorldCreate, WorldUpdate
from app.repositories.world_repository import WorldRepository


class WorldService:
    """Service layer for World operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = WorldRepository(db)
    
    def create(self, schema: WorldCreate, is_demo: bool = False) -> World:
        """Create a new world."""
        return self.repository.create(
            name=schema.name,
            description=schema.description,
            genre=schema.genre,
            visual_style=schema.visual_style,
            scale_km_per_unit=schema.scale_km_per_unit,
            is_demo=is_demo,
        )
    
    def get(self, world_id: UUID) -> Optional[World]:
        """Get a world by ID."""
        return self.repository.get(world_id)
    
    def list(self, skip: int = 0, limit: int = 100) -> List[World]:
        """List all worlds."""
        return self.repository.list(skip=skip, limit=limit)
    
    def update(self, world_id: UUID, schema: WorldUpdate) -> Optional[World]:
        """Update an existing world."""
        update_data = schema.model_dump(exclude_unset=True)
        return self.repository.update(world_id, **update_data)
    
    def delete(self, world_id: UUID) -> bool:
        """Delete a world."""
        return self.repository.delete(world_id)
    
    def count(self) -> int:
        """Count total worlds."""
        return self.repository.count()
    
    def search(self, search_term: str, skip: int = 0, limit: int = 100) -> List[World]:
        """Search worlds by name or description (case-insensitive)."""
        return self.repository.search(search_term, skip=skip, limit=limit)
    
    def count_search(self, search_term: str) -> int:
        """Count worlds matching search term."""
        return self.repository.count_search(search_term)
