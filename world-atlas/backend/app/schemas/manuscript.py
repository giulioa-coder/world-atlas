"""
Pydantic schemas for Manuscript entities.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field
import enum


class ManuscriptStatus(str, enum.Enum):
    """Status of manuscript processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ManuscriptBase(BaseModel):
    """Base schema for Manuscript."""
    
    title: str = Field(..., min_length=1, max_length=255)
    file_type: str = Field(..., pattern="^(txt|docx|pdf)$")


class ManuscriptCreate(ManuscriptBase):
    """Schema for creating a new Manuscript."""
    pass


class ManuscriptResponse(ManuscriptBase):
    """Schema for Manuscript response with all fields."""
    
    id: UUID
    world_id: UUID
    file_path: str
    word_count: Optional[int] = None
    status: ManuscriptStatus
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ChapterBase(BaseModel):
    """Base schema for Chapter."""
    
    chapter_number: Optional[int] = None
    title: Optional[str] = None


class ChapterCreate(ChapterBase):
    """Schema for creating a new Chapter."""
    
    text: str = Field(..., min_length=1)
    manuscript_id: UUID


class ChapterResponse(ChapterBase):
    """Schema for Chapter response with all fields."""
    
    id: UUID
    manuscript_id: UUID
    text: str
    word_count: Optional[int] = None
    chronological_order: Optional[int] = None
    pov_character: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProcessingResult(BaseModel):
    """Schema for manuscript processing result."""
    
    manuscript_id: str
    status: str
    message: str
    word_count: Optional[int] = None
    chapter_count: Optional[int] = None
    chapters: Optional[List[dict]] = None
