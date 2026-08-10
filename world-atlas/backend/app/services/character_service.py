"""
Character Service - Business logic for managing characters.

Handles CRUD operations and character-world relationships.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate


class CharacterService:
    """Service for managing characters in the world model."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_character(self, character_id: UUID) -> Optional[Character]:
        """Get a single character by ID."""
        result = self.db.execute(
            select(Character)
            .options(selectinload(Character.journeys))
            .where(Character.id == character_id)
        )
        return result.scalar_one_or_none()
    
    def get_characters_by_world(self, world_id: UUID) -> List[Character]:
        """Get all characters for a world."""
        result = self.db.execute(
            select(Character)
            .where(Character.world_id == world_id)
            .order_by(Character.name)
        )
        return list(result.scalars().all())
    
    def create_character(self, world_id: UUID, data: CharacterCreate) -> Character:
        """Create a new character."""
        character = Character(
            world_id=world_id,
            name=data.name,
            description=data.description,
            role=data.role,
        )
        
        self.db.add(character)
        self.db.flush()
        self.db.refresh(character)
        
        return character
    
    def update_character(
        self, 
        character_id: UUID, 
        data: CharacterUpdate
    ) -> Optional[Character]:
        """Update an existing character."""
        character = self.get_character(character_id)
        if not character:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(character, field, value)
        
        self.db.flush()
        self.db.refresh(character)
        
        return character
    
    def delete_character(self, character_id: UUID) -> bool:
        """Delete a character."""
        character = self.get_character(character_id)
        if not character:
            return False
        
        self.db.delete(character)
        self.db.commit()
        
        return True
    
    def count_by_world(self, world_id: UUID) -> int:
        """Count characters in a world."""
        result = self.db.execute(
            select(Character)
            .where(Character.world_id == world_id)
        )
        return len(list(result.scalars().all()))
