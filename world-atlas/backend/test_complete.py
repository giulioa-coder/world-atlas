"""
Test completo di tutte le funzionalità del backend World Atlas.
Esegui con: python test_complete.py
"""

from app.database import engine, Base, SessionLocal
from app.models import *
from app.services.world_service import WorldService
from app.services.location_service import LocationService
from app.services.manuscript_service import ManuscriptService
from app.services.character_service import CharacterService
from app.schemas.world import WorldCreate
from app.schemas.location import LocationCreate, LocationType
from app.schemas.manuscript import ManuscriptCreate
from app.schemas.character import CharacterCreate

def run_tests():
    print("=" * 60)
    print("WORLD ATLAS - TEST COMPLETO BACKEND")
    print("=" * 60)
    
    # Inizializzazione DB
    print("\n1. Inizializzazione database...")
    Base.metadata.create_all(bind=engine)
    print("   ✅ Tabelle create/verificate")
    
    db = SessionLocal()
    try:
        # Test World Service
        print("\n2. Test World Service...")
        world_service = WorldService(db)
        
        world_data = WorldCreate(
            name="Testaria",
            description="Mondo di test per validazione",
            genre="fantasy",
            visual_style="medieval_parchment"
        )
        world = world_service.create(world_data)
        print(f"   ✅ Mondo creato: {world.name}")
        
        worlds = world_service.list()
        print(f"   ✅ Totale mondi: {len(worlds)}")
        
        # Test Location Service
        print("\n3. Test Location Service...")
        loc_service = LocationService(db)
        
        locations_data = [
            ("Capital City", LocationType.CITY, 45.0, 12.0),
            ("North Castle", LocationType.CASTLE, 50.0, 10.0),
            ("Dark Forest", LocationType.FOREST, 40.0, 15.0),
            ("Iron Mountains", LocationType.MOUNTAIN_RANGE, 55.0, 20.0),
            ("River Port", LocationType.HARBOR, 42.0, 18.0),
        ]
        
        for name, loc_type, lat, lng in locations_data:
            loc_data = LocationCreate(
                name=name,
                location_type=loc_type,
                latitude=lat,
                longitude=lng,
                confidence=0.9,
                status='canonical'
            )
            location = loc_service.create_location(world.id, loc_data)
            print(f"   ✅ Location: {location.name} ({location.location_type.value})")
        
        all_locations = loc_service.get_locations_by_world(world.id)
        print(f"   ✅ Totale locations: {len(all_locations)}")
        
        # Test Character Service
        print("\n4. Test Character Service...")
        char_service = CharacterService(db)
        
        char_data = CharacterCreate(
            name="Hero McTesterson",
            description="Protagonista del mondo di test",
            role="protagonist"
        )
        character = char_service.create_character(world.id, char_data)
        print(f"   ✅ Personaggio creato: {character.name}")
        
        # Test Manuscript Service (solo creazione record)
        print("\n5. Test Manuscript Service...")
        manuscript_service = ManuscriptService(db)
        
        # Crea un manoscritto fittizio per test
        from app.models.manuscript import Manuscript, ManuscriptStatus
        manuscript = Manuscript(
            world_id=world.id,
            title="Test Manuscript",
            file_path="/tmp/test.txt",
            file_type="txt",
            word_count=1000,
            status=ManuscriptStatus.COMPLETED
        )
        db.add(manuscript)
        db.commit()
        db.refresh(manuscript)
        print(f"   ✅ Manoscritto creato: {manuscript.title}")
        
        # Riepilogo
        print("\n" + "=" * 60)
        print("RIEPILOGO TEST")
        print("=" * 60)
        print(f"✅ Mondi totali nel DB: {world_service.count()}")
        print(f"✅ Locations nel mondo '{world.name}': {len(all_locations)}")
        print(f"✅ Personaggi nel mondo: {len(char_service.get_characters_by_world(world.id))}")
        print(f"✅ Database: SQLite (file: world_atlas.db)")
        print("\n🎉 TUTTI I TEST SONO PASSATI!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERRORE DURANTE I TEST: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
