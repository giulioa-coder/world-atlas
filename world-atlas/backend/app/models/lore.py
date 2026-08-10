"""
LoreEntity model for world-building elements.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from app.database import JSONBOrJSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class LoreType(str, enum.Enum):
    """Types of lore entities."""
    PEOPLE = "people"
    RACE = "race"
    SPECIES = "species"
    RELIGION = "religion"
    DEITY = "deity"
    FACTION = "faction"
    CURRENCY = "currency"
    LANGUAGE = "language"
    POLITICAL_ENTITY = "political_entity"
    ORGANIZATION = "organization"
    TECHNOLOGY = "technology"
    MAGIC_SYSTEM = "magic_system"
    CUSTOM = "custom"


class LoreEntity(Base):
    """
    A lore entity represents world-building elements.
    
    This includes factions, religions, currencies, languages,
    magic systems, and other non-geographical entities.
    """
    
    __tablename__ = "lore_entities"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[LoreType] = mapped_column(
        SQLEnum(LoreType), 
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    extra_data: Mapped[Dict[str, Any]] = mapped_column(
        JSONBOrJSON, 
        default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="lore_entities")
    
    def __repr__(self) -> str:
        return f"<LoreEntity(id={self.id}, name='{self.name}', type={self.entity_type})>"
