"""
Character and CharacterJourney models.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Character(Base):
    """
    A character in the world.
    
    Characters can travel between locations, and their journeys
    are tracked for timeline visualization.
    """
    
    __tablename__ = "characters"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    role: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="characters")
    journeys = relationship(
        "CharacterJourney", 
        back_populates="character", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Character(id={self.id}, name='{self.name}')>"


class CharacterJourney(Base):
    """
    A journey segment for a character.
    
    Tracks movement from one location to another, including
    travel mode, duration, and distance.
    """
    
    __tablename__ = "character_journeys"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"), 
        nullable=False
    )
    chapter_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE"), 
        default=None
    )
    origin_location_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("locations.id"), 
        default=None
    )
    destination_location_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("locations.id"), 
        default=None
    )
    route_description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    travel_mode: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    stated_duration_days: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), 
        default=None
    )
    inferred_duration_days: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), 
        default=None
    )
    distance_km: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), 
        default=None
    )
    confidence: Mapped[float] = mapped_column(Numeric(3, 2), default=0.5)
    notes: Mapped[Optional[str]] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    character = relationship("Character", back_populates="journeys")
    chapter = relationship("Chapter", back_populates="character_journeys")
    origin = relationship("Location", foreign_keys=[origin_location_id])
    destination = relationship("Location", foreign_keys=[destination_location_id])
    
    def __repr__(self) -> str:
        return f"<CharacterJourney(character={self.character_id}, chapter={self.chapter_id})>"
