"""
Seed script for creating the demo world "Elarion".

This script populates the database with a sample fictional world
containing locations, roads, and basic geographical data.
"""

import asyncio
import sys
from pathlib import Path
from uuid import UUID

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.database import get_database_url
from app.models.world import World
from app.models.location import Location, LocationType, LocationStatus
from app.models.manuscript import Chapter
from app.schemas.location import LocationCreate

# Demo world data
ELARION_DATA = {
    "world": {
        "name": "Elarion",
        "description": "A fantasy realm of ancient kingdoms, mystical forests, and towering mountains. The land is divided between the prosperous southern kingdoms and the harsh northern wastes.",
        "genre": "fantasy",
        "visual_style": "medieval_parchment",
    },
    "locations": [
        # Kingdoms & Major Cities
        {
            "name": "Aurelia",
            "location_type": LocationType.KINGDOM,
            "latitude": 45.0,
            "longitude": 50.0,
            "description": "The golden kingdom of Aurelia, ruled by the House of Valorian. Known for its wealth, culture, and powerful army.",
            "importance": 5,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Aurelis",
            "location_type": LocationType.CAPITAL,
            "latitude": 44.5,
            "longitude": 51.0,
            "description": "The magnificent capital city of Aurelia, built on seven hills overlooking the Serath River. Home to the Crystal Palace.",
            "importance": 5,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Port Neris",
            "location_type": LocationType.PORT,
            "latitude": 42.0,
            "longitude": 55.0,
            "description": "The largest port city in Elarion, gateway to the Eastern Seas. A bustling hub of trade and commerce.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        
        # Northern Regions
        {
            "name": "Iron Mountains",
            "location_type": LocationType.MOUNTAIN_RANGE,
            "latitude": 55.0,
            "longitude": 45.0,
            "description": "A formidable mountain range separating the northern wastes from the southern kingdoms. Rich in iron and mithril deposits.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Castle Veyr",
            "location_type": LocationType.CASTLE,
            "latitude": 53.0,
            "longitude": 47.0,
            "description": "An ancient fortress carved into the Iron Mountains. Once held by the dwarf kings, now abandoned.",
            "importance": 3,
            "status": LocationStatus.CANONICAL,
        },
        
        # Forests & Wilderness
        {
            "name": "Black Forest",
            "location_type": LocationType.FOREST,
            "latitude": 48.0,
            "longitude": 35.0,
            "description": "A dark and mysterious forest where sunlight rarely penetrates the canopy. Home to ancient spirits and dangerous creatures.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Village Elden",
            "location_type": LocationType.VILLAGE,
            "latitude": 47.5,
            "longitude": 36.0,
            "description": "A small village on the edge of the Black Forest. Its inhabitants are woodcutters and hunters.",
            "importance": 2,
            "status": LocationStatus.CANONICAL,
        },
        
        # Rivers & Water Bodies
        {
            "name": "River Serath",
            "location_type": LocationType.RIVER,
            "latitude": 43.0,
            "longitude": 50.0,
            "description": "The great river that flows from the Iron Mountains through Aurelia to the Eastern Sea.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Lake Mirath",
            "location_type": LocationType.LAKE,
            "latitude": 50.0,
            "longitude": 40.0,
            "description": "A serene lake nestled in the foothills of the Iron Mountains. Said to be blessed by the moon goddess.",
            "importance": 3,
            "status": LocationStatus.CANONICAL,
        },
        
        # Additional Points of Interest
        {
            "name": "The Shattered Plains",
            "location_type": LocationType.BATTLEFIELD,
            "latitude": 46.0,
            "longitude": 42.0,
            "description": "Site of the great battle between the human kingdoms and the shadow armies. The land still bears scars of magic.",
            "importance": 3,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Temple of Dawn",
            "location_type": LocationType.TEMPLE,
            "latitude": 44.0,
            "longitude": 48.0,
            "description": "An ancient temple dedicated to the sun god. Pilgrims travel here from across the realm.",
            "importance": 3,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Shadowmere",
            "location_type": LocationType.MAGICAL_AREA,
            "latitude": 58.0,
            "longitude": 30.0,
            "description": "A cursed swamp in the far north where reality bends and strange creatures dwell.",
            "importance": 4,
            "status": LocationStatus.INFERRED,
        },
    ],
    "chapters": [
        {
            "title": "The Journey Begins",
            "chapter_number": 1,
            "text": "Kael stood at the gates of Aurelis, looking south toward the distant Iron Mountains. His journey would take him through the Black Forest, across the Shattered Plains, and eventually to the shores of Lake Mirath...",
            "chronological_order": 1,
        },
        {
            "title": "Through the Forest",
            "chapter_number": 2,
            "text": "The Black Forest lived up to its name. Darkness enveloped Kael as he passed Village Elden, where the villagers warned him of the shadows that moved between the trees...",
            "chronological_order": 2,
        },
        {
            "title": "The Ancient Castle",
            "chapter_number": 3,
            "text": "Castle Veyr rose before him, its stone walls weathered by centuries of mountain winds. Somewhere within these ruins lay the artifact he sought...",
            "chronological_order": 3,
        },
    ],
    "characters": [
        {"name": "Kael", "description": "A young warrior from Aurelia, seeking to restore his family's honor."},
        {"name": "Mira", "description": "A mysterious mage from the Temple of Dawn with knowledge of ancient magic."},
        {"name": "Toren", "description": "A grizzled veteran who knows the secrets of the Iron Mountains."},
    ],
}


async def seed_elarion():
    """Seed the Elarion demo world."""
    
    # Get database URL from environment or use default
    database_url = get_database_url()
    
    # Create async engine
    engine = create_async_engine(database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Check if Elarion already exists
            result = await session.execute(
                select(World).where(World.name == "Elarion")
            )
            existing_world = result.scalar_one_or_none()
            
            if existing_world:
                print("✓ Elarion world already exists. Skipping seed.")
                return
            
            # Create the world
            world = World(
                name=ELARION_DATA["world"]["name"],
                description=ELARION_DATA["world"]["description"],
                genre=ELARION_DATA["world"]["genre"],
                visual_style=ELARION_DATA["world"]["visual_style"],
            )
            session.add(world)
            await session.flush()
            await session.refresh(world)
            
            print(f"✓ Created world: {world.name} (ID: {world.id})")
            
            # Create locations
            location_ids = {}
            for loc_data in ELARION_DATA["locations"]:
                location = Location(
                    world_id=world.id,
                    name=loc_data["name"],
                    location_type=loc_data["location_type"],
                    latitude=loc_data.get("latitude"),
                    longitude=loc_data.get("longitude"),
                    description=loc_data.get("description"),
                    importance=loc_data.get("importance", 1),
                    status=loc_data.get("status", LocationStatus.CANONICAL),
                    confidence=0.95,
                )
                session.add(location)
                location_ids[loc_data["name"]] = location.id
                print(f"  → Created location: {location.name}")
            
            await session.flush()
            print(f"✓ Created {len(location_ids)} locations")
            
            # Create chapters (without manuscript for demo)
            # In a real scenario, these would come from a manuscript
            print(f"✓ Demo world ready with {len(ELARION_DATA['chapters'])} sample chapters defined")
            
            # Commit everything
            await session.commit()
            
            print("\n" + "="*50)
            print("ELARION DEMO WORLD CREATED SUCCESSFULLY")
            print("="*50)
            print(f"\nWorld ID: {world.id}")
            print(f"Locations: {len(location_ids)}")
            print("\nTo use this demo world:")
            print(f"  - Access via API: /api/v1/worlds/{world.id}/")
            print(f"  - View locations: /api/v1/locations/worlds/{world.id}/")
            print("\n")
            
        except Exception as e:
            await session.rollback()
            print(f"✗ Error seeding Elarion: {e}")
            raise


def main():
    """Main entry point."""
    print("🌍 Seeding Elarion demo world...")
    asyncio.run(seed_elarion())


if __name__ == "__main__":
    main()
