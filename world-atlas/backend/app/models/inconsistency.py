"""
Inconsistency model for tracking geographical contradictions.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum


class InconsistencyType(str, enum.Enum):
    """Types of inconsistencies."""
    TRAVEL_TIME = "travel_time"
    DIRECTION = "direction"
    DISTANCE = "distance"
    IMPOSSIBLE_GEOGRAPHY = "impossible_geography"
    CONTRADICTORY_POSITION = "contradictory_position"


class InconsistencySeverity(str, enum.Enum):
    """Severity levels for inconsistencies."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InconsistencyStatus(str, enum.Enum):
    """Status of inconsistency resolution."""
    OPEN = "open"
    DISMISSED = "dismissed"
    RESOLVED = "resolved"


class Inconsistency(Base):
    """
    A detected inconsistency in the world model.
    
    The system detects potential contradictions but never
    automatically declares them as errors. Authors review
    and resolve them.
    """
    
    __tablename__ = "inconsistencies"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    inconsistency_type: Mapped[InconsistencyType] = mapped_column(
        SQLEnum(InconsistencyType), 
        nullable=False
    )
    severity: Mapped[InconsistencySeverity] = mapped_column(
        SQLEnum(InconsistencySeverity), 
        default=InconsistencySeverity.MEDIUM
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    related_entities: Mapped[List[str]] = mapped_column(
        JSONB, 
        default=list
    )  # List of entity IDs
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, default=None)
    status: Mapped[InconsistencyStatus] = mapped_column(
        SQLEnum(InconsistencyStatus), 
        default=InconsistencyStatus.OPEN
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="inconsistencies")
    
    def __repr__(self) -> str:
        return f"<Inconsistency(id={self.id}, type={self.inconsistency_type}, status={self.status})>"
