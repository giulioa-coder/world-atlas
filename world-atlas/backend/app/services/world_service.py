"""
World service for business logic operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.world import World
from app.schemas.world import WorldCreate, WorldUpdate


class WorldService:
    """Service layer for World operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, schema: WorldCreate, is_demo: bool = False) -> World:
        """Create a new world."""
        world = World(
            name=schema.name,
            description=schema.description,
            genre=schema.genre,
            visual_style=schema.visual_style,
            scale_km_per_unit=schema.scale_km_per_unit,
            is_demo=is_demo,
        )
        self.db.add(world)
        self.db.commit()
        self.db.refresh(world)
        return world
    
    def get(self, world_id: UUID) -> Optional[World]:
        """Get a world by ID."""
        return self.db.query(World).filter(World.id == world_id).first()
    
    def list(self, skip: int = 0, limit: int = 100) -> List[World]:
        """List all worlds."""
        return self.db.query(World).offset(skip).limit(limit).all()
    
    def update(self, world_id: UUID, schema: WorldUpdate) -> Optional[World]:
        """Update an existing world."""
        world = self.get(world_id)
        if not world:
            return None
        
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(world, field, value)
        
        self.db.commit()
        self.db.refresh(world)
        return world
    
    def delete(self, world_id: UUID) -> bool:
        """Delete a world."""
        world = self.get(world_id)
        if not world:
            return False
        
        self.db.delete(world)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Count total worlds."""
        return self.db.query(World).count()
