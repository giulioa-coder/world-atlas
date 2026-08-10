"""
Pydantic schemas for Character entities.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class CharacterBase(BaseModel):
    """Base schema for Character."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    role: Optional[str] = Field(None, max_length=100)


class CharacterCreate(CharacterBase):
    """Schema for creating a new Character."""
    pass


class CharacterUpdate(BaseModel):
    """Schema for updating an existing Character."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    role: Optional[str] = Field(None, max_length=100)


class CharacterResponse(CharacterBase):
    """Schema for Character response with all fields."""
    
    id: UUID
    world_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
