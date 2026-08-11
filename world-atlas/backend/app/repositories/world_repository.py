"""
World repository for database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.world import World
from app.repositories.base import Repository


class WorldRepository(Repository[World]):
    """Repository for World model operations."""
    
    def __init__(self, db: Session):
        super().__init__(model=World, db=db)
    
    def get_by_name(self, name: str) -> Optional[World]:
        """Get a world by name."""
        return self.db.query(World).filter(World.name == name).first()
    
    def list_with_filters(
        self, 
        skip: int = 0, 
        limit: int = 100,
        genre: Optional[str] = None,
        is_demo: Optional[bool] = None,
    ) -> List[World]:
        """List worlds with optional filters."""
        query = self.db.query(World)
        
        if genre:
            query = query.filter(World.genre == genre)
        
        if is_demo is not None:
            query = query.filter(World.is_demo == is_demo)
        
        return query.offset(skip).limit(limit).all()
    
    def search(self, search_term: str, skip: int = 0, limit: int = 100) -> List[World]:
        """Search worlds by name or description (case-insensitive)."""
        search_pattern = f"%{search_term}%"
        return (
            self.db.query(World)
            .filter(
                (World.name.ilike(search_pattern)) | 
                (World.description.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_search(self, search_term: str) -> int:
        """Count worlds matching search term."""
        search_pattern = f"%{search_term}%"
        return (
            self.db.query(World)
            .filter(
                (World.name.ilike(search_pattern)) | 
                (World.description.ilike(search_pattern))
            )
            .count()
        )
