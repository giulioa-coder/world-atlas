"""
Manuscript and Chapter models.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class ManuscriptStatus(str, enum.Enum):
    """Status of manuscript processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Manuscript(Base):
    """
    A manuscript represents an uploaded book draft or text document.
    
    Manuscripts are parsed to extract geographical information and
    populate the world model.
    """
    
    __tablename__ = "manuscripts"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    status: Mapped[ManuscriptStatus] = mapped_column(
        SQLEnum(ManuscriptStatus), 
        default=ManuscriptStatus.PENDING
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, default=None)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        default=None
    )
    
    # Relationships
    world = relationship("World", back_populates="manuscripts")
    chapters = relationship(
        "Chapter", 
        back_populates="manuscript", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Manuscript(id={self.id}, title='{self.title}')>"


class Chapter(Base):
    """
    A chapter represents a section of a manuscript.
    
    Chapters are the primary unit for entity extraction and
    geographical analysis.
    """
    
    __tablename__ = "chapters"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    manuscript_id: Mapped[UUID] = mapped_column(
        ForeignKey("manuscripts.id", ondelete="CASCADE"), 
        nullable=False
    )
    chapter_number: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    title: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    chronological_order: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    pov_character: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    start_index: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    end_index: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    manuscript = relationship("Manuscript", back_populates="chapters")
    location_mentions = relationship(
        "LocationMention", 
        back_populates="chapter", 
        cascade="all, delete-orphan"
    )
    character_journeys = relationship(
        "CharacterJourney", 
        back_populates="chapter", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Chapter(id={self.id}, number={self.chapter_number})>"
