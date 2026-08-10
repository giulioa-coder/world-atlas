"""
WorldVersion model for tracking world state history.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from app.database import JSONBOrJSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WorldVersion(Base):
    """
    A snapshot of world state at a point in time.
    
    Enables version history, comparison, and restoration
    of previous world states.
    """
    
    __tablename__ = "world_versions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_data: Mapped[Dict[str, Any]] = mapped_column(
        JSONBOrJSON, 
        nullable=False
    )
    change_summary: Mapped[Optional[str]] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="versions")
    
    def __repr__(self) -> str:
        return f"<WorldVersion(world={self.world_id}, version={self.version_number})>"
