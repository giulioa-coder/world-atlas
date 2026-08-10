"""
API v1 routers.
"""

from app.api.v1.worlds import router as worlds_router
from app.api.v1.locations import router as locations_router
from app.api.v1.manuscripts import router as manuscripts_router
from app.api.v1.characters import router as characters_router
from app.api.v1.timeline import router as timeline_router
from app.api.v1.export import router as export_router

__all__ = [
    "worlds_router",
    "locations_router",
    "manuscripts_router",
    "characters_router",
    "timeline_router",
    "export_router",
]
