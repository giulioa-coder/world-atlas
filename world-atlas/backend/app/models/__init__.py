"""
SQLAlchemy models for the World Atlas application.
"""

from app.database import Base
from app.models.world import World
from app.models.manuscript import Manuscript, Chapter
from app.models.location import Location, LocationMention, Region, Road, Border
from app.models.character import Character, CharacterJourney
from app.models.lore import LoreEntity
from app.models.poi import POISuggestion
from app.models.inconsistency import Inconsistency
from app.models.version import WorldVersion

__all__ = [
    "Base",
    "World",
    "Manuscript",
    "Chapter",
    "Location",
    "LocationMention",
    "Region",
    "Road",
    "Border",
    "Character",
    "CharacterJourney",
    "LoreEntity",
    "POISuggestion",
    "Inconsistency",
    "WorldVersion",
]
