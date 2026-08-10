"""
World model - the root entity containing all geographical data.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Text, DateTime, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class World(Base):
    """
    A world represents a complete fictional geography.
    
    This is the root entity that contains all locations, characters,
    manuscripts, and other geographical data.
    """
    
    __tablename__ = "worlds"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    genre: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    visual_style: Mapped[str] = mapped_column(
        String(100), 
        default="medieval_parchment"
    )
    scale_km_per_unit: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), 
        default=50.0
    )
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    locations = relationship(
        "Location", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    manuscripts = relationship(
        "Manuscript", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    characters = relationship(
        "Character", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    regions = relationship(
        "Region", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    roads = relationship(
        "Road", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    borders = relationship(
        "Border", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    lore_entities = relationship(
        "LoreEntity", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    poi_suggestions = relationship(
        "POISuggestion", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    inconsistencies = relationship(
        "Inconsistency", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    versions = relationship(
        "WorldVersion", 
        back_populates="world", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<World(id={self.id}, name='{self.name}')>"
