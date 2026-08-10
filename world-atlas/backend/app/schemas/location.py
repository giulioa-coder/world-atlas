"""
Pydantic schemas for Location entities.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field
import enum


class LocationType(str, enum.Enum):
    """Types of geographical locations."""
    CONTINENT = "continent"
    COUNTRY = "country"
    KINGDOM = "kingdom"
    REGION = "region"
    PROVINCE = "province"
    CITY = "city"
    TOWN = "town"
    VILLAGE = "village"
    CASTLE = "castle"
    FORTRESS = "fortress"
    CAPITAL = "capital"
    HARBOR = "harbor"
    PORT = "port"
    INN = "inn"
    TEMPLE = "temple"
    RUIN = "ruin"
    CAVE = "cave"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    MOUNTAIN_RANGE = "mountain_range"
    RIVER = "river"
    LAKE = "lake"
    SEA = "sea"
    OCEAN = "ocean"
    ISLAND = "island"
    LANDMARK = "landmark"
    BATTLEFIELD = "battlefield"
    MAGICAL_AREA = "magical_area"
    CUSTOM = "custom"


class LocationStatus(str, enum.Enum):
    """Status of location data confidence."""
    CANONICAL = "canonical"
    INFERRED = "inferred"
    SUGGESTED = "suggested"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class LocationBase(BaseModel):
    """Base schema for Location."""
    
    name: str = Field(..., min_length=1, max_length=255)
    location_type: LocationType
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    elevation: Optional[int] = None
    description: Optional[str] = None
    visual_description: Optional[str] = None
    importance: int = Field(1, ge=1, le=5)
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class LocationCreate(LocationBase):
    """Schema for creating a new Location."""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating an existing Location."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    location_type: Optional[LocationType] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    elevation: Optional[int] = None
    description: Optional[str] = None
    visual_description: Optional[str] = None
    importance: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[LocationStatus] = None
    extra_data: Optional[Dict[str, Any]] = None


class LocationMentionBase(BaseModel):
    """Base schema for Location Mention."""
    
    chapter_id: UUID
    text_span: str = Field(..., min_length=1)
    context: Optional[str] = None
    paragraph_index: Optional[int] = None
    sentence_index: Optional[int] = None
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    extraction_method: str = "manual"


class LocationMentionCreate(LocationMentionBase):
    """Schema for creating a location mention."""
    pass


class LocationMentionResponse(LocationMentionBase):
    """Schema for location mention response."""
    
    id: UUID
    location_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class LocationResponse(LocationBase):
    """Schema for Location response with all fields."""
    
    id: UUID
    world_id: UUID
    confidence: float
    status: LocationStatus
    first_appearance_chapter_id: Optional[UUID] = None
    last_appearance_chapter_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    mentions: Optional[List[LocationMentionResponse]] = []
    
    class Config:
        from_attributes = True


class LocationListResponse(BaseModel):
    """Schema for list of locations."""
    
    items: List[LocationResponse]
    total: int
