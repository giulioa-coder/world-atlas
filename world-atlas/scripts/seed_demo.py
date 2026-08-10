#!/usr/bin/env python3
"""
Seed script to create the demo world "Elarion".

Run this after setting up the database to populate it with
sample data for testing and demonstration.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.world import World
from app.models.location import Location, LocationType, LocationStatus
from app.models.character import Character


def create_demo_world(db: Session):
    """Create the Elarion demo world with sample locations and characters."""
    
    # Check if demo world already exists
    existing = db.query(World).filter(World.name == "Elarion").first()
    if existing:
        print("Demo world 'Elarion' already exists. Skipping.")
        return existing
    
    # Create world
    world = World(
        name="Elarion",
        description="A fantasy realm of ancient kingdoms, mystical forests, and towering mountains.",
        genre="fantasy",
        visual_style="medieval_parchment",
        scale_km_per_unit=50.0,
        is_demo=True,
    )
    db.add(world)
    db.commit()
    db.refresh(world)
    
    print(f"Created demo world: {world.name} (ID: {world.id})")
    
    # Create locations
    locations_data = [
        {
            "name": "Aurelia",
            "location_type": LocationType.CAPITAL,
            "latitude": 45.0,
            "longitude": 50.0,
            "description": "The gleaming capital city of the Kingdom of Aurelia, known for its golden spires.",
            "importance": 5,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Black Forest",
            "location_type": LocationType.FOREST,
            "latitude": 30.0,
            "longitude": 35.0,
            "description": "An ancient, dense forest shrouded in perpetual twilight. Home to mysterious creatures.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Iron Mountains",
            "location_type": LocationType.MOUNTAIN_RANGE,
            "latitude": 60.0,
            "longitude": 70.0,
            "description": "A formidable mountain range rich in iron ore, home to dwarf clans.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "River Serath",
            "location_type": LocationType.RIVER,
            "latitude": 40.0,
            "longitude": 45.0,
            "description": "The great river that flows from the Iron Mountains to the southern sea.",
            "importance": 3,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Castle Veyr",
            "location_type": LocationType.CASTLE,
            "latitude": 50.0,
            "longitude": 55.0,
            "description": "An ancient fortress perched on a cliff overlooking the River Serath.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Port Neris",
            "location_type": LocationType.PORT,
            "latitude": 25.0,
            "longitude": 50.0,
            "description": "A bustling port city on the southern coast, gateway to distant lands.",
            "importance": 4,
            "status": LocationStatus.CANONICAL,
        },
        {
            "name": "Village Elden",
            "location_type": LocationType.VILLAGE,
            "latitude": 35.0,
            "longitude": 40.0,
            "description": "A small farming village on the edge of the Black Forest.",
            "importance": 2,
            "status": LocationStatus.CANONICAL,
        },
    ]
    
    for loc_data in locations_data:
        location = Location(
            world_id=world.id,
            **loc_data,
            confidence=1.0,
        )
        db.add(location)
    
    db.commit()
    print(f"Created {len(locations_data)} locations in Elarion")
    
    # Create characters
    characters_data = [
        {
            "name": "Kael",
            "description": "A young warrior from Village Elden seeking adventure.",
            "role": "protagonist",
        },
        {
            "name": "Mira",
            "description": "A mysterious mage with knowledge of ancient secrets.",
            "role": "protagonist",
        },
        {
            "name": "Toren",
            "description": "The aging king of Aurelia, facing threats from all sides.",
            "role": "supporting",
        },
    ]
    
    for char_data in characters_data:
        character = Character(
            world_id=world.id,
            **char_data,
        )
        db.add(character)
    
    db.commit()
    print(f"Created {len(characters_data)} characters in Elarion")
    
    return world


def main():
    """Main entry point."""
    print("Seeding demo world 'Elarion'...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create session and seed data
    db = SessionLocal()
    try:
        world = create_demo_world(db)
        print(f"\n✓ Demo world seeded successfully!")
        print(f"  World ID: {world.id}")
        print(f"  Locations: 7")
        print(f"  Characters: 3")
    finally:
        db.close()


if __name__ == "__main__":
    main()
