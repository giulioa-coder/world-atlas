"""
Repository pattern implementation for database operations.
"""

from app.repositories.base import Repository
from app.repositories.world_repository import WorldRepository
from app.repositories.location_repository import LocationRepository
from app.repositories.manuscript_repository import ManuscriptRepository
from app.repositories.character_repository import CharacterRepository

__all__ = [
    "Repository",
    "WorldRepository",
    "LocationRepository",
    "ManuscriptRepository",
    "CharacterRepository",
]
