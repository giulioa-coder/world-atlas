"""
Pydantic schemas for World entities.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class WorldBase(BaseModel):
    """Base schema for World."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    genre: Optional[str] = Field(None, max_length=100)
    visual_style: str = "medieval_parchment"
    scale_km_per_unit: Optional[float] = 50.0


class WorldCreate(WorldBase):
    """Schema for creating a new World."""
    pass


class WorldUpdate(BaseModel):
    """Schema for updating an existing World."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    genre: Optional[str] = None
    visual_style: Optional[str] = None
    scale_km_per_unit: Optional[float] = None


class WorldResponse(WorldBase):
    """Schema for World response with all fields."""
    
    id: UUID
    is_demo: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorldListResponse(BaseModel):
    """Schema for list of worlds."""
    
    items: List[WorldResponse]
    total: int
