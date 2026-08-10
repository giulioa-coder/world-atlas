"""
Character repository for database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.character import Character, CharacterJourney
from app.repositories.base import Repository


class CharacterRepository(Repository[Character]):
    """Repository for Character model operations."""
    
    def __init__(self, db: Session):
        super().__init__(model=Character, db=db)
    
    def get_by_world(self, world_id: UUID) -> List[Character]:
        """Get all characters for a specific world."""
        return self.db.query(Character).filter(Character.world_id == world_id).all()
    
    def search_by_name(self, world_id: UUID, search_term: str) -> List[Character]:
        """Search characters by name within a world."""
        search_pattern = f"%{search_term}%"
        return self.db.query(Character).filter(
            Character.world_id == world_id,
            Character.name.ilike(search_pattern)
        ).all()
    
    def get_with_journeys(self, character_id: UUID) -> Optional[Character]:
        """Get a character with their journeys."""
        return (
            self.db.query(Character)
            .filter(Character.id == character_id)
            .first()
        )
    
    def count_by_world(self, world_id: UUID) -> int:
        """Count characters for a specific world."""
        return self.db.query(Character).filter(
            Character.world_id == world_id
        ).count()


class CharacterJourneyRepository:
    """Repository for CharacterJourney model operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.model = CharacterJourney
    
    def get_by_character(self, character_id: UUID) -> List[CharacterJourney]:
        """Get all journeys for a character."""
        return self.db.query(CharacterJourney).filter(
            CharacterJourney.character_id == character_id
        ).all()
    
    def get_by_chapter(self, chapter_id: UUID) -> List[CharacterJourney]:
        """Get all journeys for a chapter."""
        return self.db.query(CharacterJourney).filter(
            CharacterJourney.chapter_id == chapter_id
        ).all()
    
    def get_by_world(self, world_id: UUID) -> List[CharacterJourney]:
        """Get all journeys for a world (via character)."""
        return (
            self.db.query(CharacterJourney)
            .join(Character)
            .filter(Character.world_id == world_id)
            .all()
        )
    
    def create_journey(self, **kwargs) -> CharacterJourney:
        """Create a new journey."""
        journey = CharacterJourney(**kwargs)
        self.db.add(journey)
        self.db.commit()
        self.db.refresh(journey)
        return journey
    
    def update_journey(
        self, 
        journey_id: UUID, 
        **kwargs
    ) -> Optional[CharacterJourney]:
        """Update a journey."""
        journey = self.db.query(CharacterJourney).filter(
            CharacterJourney.id == journey_id
        ).first()
        
        if not journey:
            return None
        
        for field, value in kwargs.items():
            setattr(journey, field, value)
        
        self.db.commit()
        self.db.refresh(journey)
        return journey
    
    def delete_journey(self, journey_id: UUID) -> bool:
        """Delete a journey."""
        journey = self.db.query(CharacterJourney).filter(
            CharacterJourney.id == journey_id
        ).first()
        
        if not journey:
            return False
        
        self.db.delete(journey)
        self.db.commit()
        return True
