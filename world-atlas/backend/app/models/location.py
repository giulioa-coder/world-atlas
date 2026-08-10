"""
Location, Region, Road, and Border models.

These models represent the core geographical entities in the world.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import (
    String, Text, DateTime, Integer, Float, ForeignKey, 
    Numeric, Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base, JSONBOrJSON


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
    CANONICAL = "canonical"  # Author-approved
    INFERRED = "inferred"    # AI-inferred from text
    SUGGESTED = "suggested"  # AI suggestion, pending review
    REJECTED = "rejected"    # Explicitly rejected
    UNKNOWN = "unknown"      # Position unknown


class Location(Base):
    """
    A geographical location in the world.
    
    Locations can be anything from continents to individual buildings.
    Each location has optional coordinates and confidence scoring.
    """
    
    __tablename__ = "locations"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location_type: Mapped[LocationType] = mapped_column(
        SQLEnum(LocationType), 
        nullable=False
    )
    latitude: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 6), 
        default=None
    )
    longitude: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 6), 
        default=None
    )
    elevation: Mapped[Optional[int]] = mapped_column(
        Integer, 
        default=None
    )  # meters
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    visual_description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    importance: Mapped[int] = mapped_column(Integer, default=1)  # 1-5 scale
    confidence: Mapped[float] = mapped_column(Numeric(3, 2), default=0.5)
    status: Mapped[LocationStatus] = mapped_column(
        SQLEnum(LocationStatus), 
        default=LocationStatus.INFERRED
    )
    first_appearance_chapter_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("chapters.id"), 
        default=None
    )
    last_appearance_chapter_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("chapters.id"), 
        default=None
    )
    extra_data: Mapped[Dict[str, Any]] = mapped_column(
        JSONBOrJSON, 
        default=dict
    )
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
    world = relationship("World", back_populates="locations")
    mentions = relationship(
        "LocationMention", 
        back_populates="location", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Location(id={self.id}, name='{self.name}', type={self.location_type})>"


class LocationMention(Base):
    """
    Evidence of a location mention in a chapter.
    
    Tracks the source text for every extracted location, enabling
    authors to verify AI extractions.
    """
    
    __tablename__ = "location_mentions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    location_id: Mapped[UUID] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE"), 
        nullable=False
    )
    chapter_id: Mapped[UUID] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE"), 
        nullable=False
    )
    text_span: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[Optional[str]] = mapped_column(Text, default=None)
    paragraph_index: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    sentence_index: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    confidence: Mapped[float] = mapped_column(Numeric(3, 2), default=0.5)
    extraction_method: Mapped[str] = mapped_column(String(50), default="ai")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    location = relationship("Location", back_populates="mentions")
    chapter = relationship("Chapter", back_populates="location_mentions")
    
    def __repr__(self) -> str:
        return f"<LocationMention(location={self.location_id}, chapter={self.chapter_id})>"


class Region(Base):
    """
    A geographical region with polygonal boundaries.
    
    Regions can represent kingdoms, provinces, forests, or any
    area with defined borders.
    """
    
    __tablename__ = "regions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    region_type: Mapped[str] = mapped_column(String(50), nullable=False)
    geometry: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONBOrJSON, 
        default=None
    )  # GeoJSON polygon
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    political_status: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    parent_region_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("regions.id"), 
        default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="regions")
    parent = relationship("Region", remote_side=[id], backref="sub_regions")
    
    def __repr__(self) -> str:
        return f"<Region(id={self.id}, name='{self.name}')>"


class Road(Base):
    """
    A road or route between two locations.
    
    Roads can represent trade routes, paths, or any connection
    between geographical points.
    """
    
    __tablename__ = "roads"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    origin_location_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("locations.id"), 
        default=None
    )
    destination_location_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("locations.id"), 
        default=None
    )
    geometry: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONBOrJSON, 
        default=None
    )  # GeoJSON line string
    estimated_distance_km: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), 
        default=None
    )
    terrain_type: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    travel_modes: Mapped[Optional[list]] = mapped_column(
        JSONBOrJSON, 
        default=None
    )  # ['walking', 'horse', 'cart']
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="roads")
    origin = relationship("Location", foreign_keys=[origin_location_id])
    destination = relationship("Location", foreign_keys=[destination_location_id])
    
    def __repr__(self) -> str:
        return f"<Road(id={self.id}, from={self.origin_location_id} to={self.destination_location_id})>"


class Border(Base):
    """
    A border between two regions.
    
    Borders can be natural (rivers, mountains) or political
    (kingdom boundaries).
    """
    
    __tablename__ = "borders"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    world_id: Mapped[UUID] = mapped_column(
        ForeignKey("worlds.id", ondelete="CASCADE"), 
        nullable=False
    )
    region_a_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("regions.id"), 
        default=None
    )
    region_b_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("regions.id"), 
        default=None
    )
    geometry: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONBOrJSON, 
        default=None
    )  # GeoJSON line string
    status: Mapped[Optional[str]] = mapped_column(String(50), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )
    
    # Relationships
    world = relationship("World", back_populates="borders")
    region_a = relationship("Region", foreign_keys=[region_a_id])
    region_b = relationship("Region", foreign_keys=[region_b_id])
    
    def __repr__(self) -> str:
        return f"<Border(id={self.id}, between={self.region_a_id} and {self.region_b_id})>"
