"""
Test script for manuscript parsing functionality.

Creates a sample text file and tests the parsing pipeline.
"""

import sys
import tempfile
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.parsing import ManuscriptParser
from app.parsing.chapter_detector import ChapterDetector


def create_sample_manuscript():
    """Create a sample manuscript for testing."""
    
    sample_text = """
The Kingdom of Aethelgard

Prologue: The Beginning

In the beginning, there was only darkness. The gods shaped the world from the void, creating the Iron Mountains in the north and the Black Forest in the south. Between them flowed the River Serath, bringing life to the land.

Chapter 1: The Journey Begins

Kael stood at the gates of Winterfell, looking north toward the Iron Mountains. The castle's stone walls gleamed white in the morning sun. He had traveled three days from Castle Veyr to reach this place.

"The road ahead is dangerous," warned Mira, his companion. She pointed east toward the distant peaks. "The mountains are treacherous this time of year."

They would need to follow the King's Road northeast for two days before reaching the village of Elden. From there, the journey to Port Neris would take another week by horse.

Chapter 2: The Black Forest

The forest loomed before them, dark and ancient. Trees taller than any cathedral stretched toward the sky, their branches forming a canopy that blocked out the sun.

"This is where the old magic lives," Kael whispered.

Mira nodded. "Legends say the first elves settled here, five thousand years ago. Before the humans came with their kingdoms and castles."

They entered the forest, following a narrow path that wound west toward the coast. Somewhere beyond the trees lay the Sea of Storms, and beyond that, the mysterious continent of Zandor.

Chapter 3: Port Neris

After five days of travel, they finally emerged from the forest. Port Neris sprawled before them, its harbor filled with ships from across the known world.

"The Aurelian fleet docks here," Mira explained. "Their capital, Aurelia, lies two hundred miles to the southeast. A fortnight's ride on good roads."

Kael looked out at the water. Somewhere to the northwest, beyond the horizon, lay the Dragon Isles. No map showed what lay beyond those mist-shrouded islands.

Epilogue: The Road Ahead

Their journey was far from over. Beyond Port Neris lay uncharted lands, forgotten ruins, and dangers yet unknown. But for now, they would rest.

Tomorrow, they would sail east toward destiny.
"""
    
    return sample_text


def test_parsing():
    """Test the manuscript parsing pipeline."""
    
    print("=" * 60)
    print("MANUSCRIPT PARSING TEST")
    print("=" * 60)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(create_sample_manuscript())
        temp_path = f.name
    
    try:
        # Test parser
        print("\n1. Testing ManuscriptParser...")
        parser = ManuscriptParser()
        
        result = parser.parse_with_chapters(temp_path)
        
        print(f"   ✓ File parsed successfully")
        print(f"   Total words: {result['word_count']}")
        print(f"   Chapters detected: {result['chapter_count']}")
        
        # Test chapter detector
        print("\n2. Testing ChapterDetector...")
        detector = ChapterDetector()
        boundaries = detector.detect(create_sample_manuscript())
        
        print(f"   Boundaries found: {len(boundaries)}")
        for i, boundary in enumerate(boundaries[:5]):  # Show first 5
            print(f"   - {boundary.pattern_type}: Chapter {boundary.chapter_number} '{boundary.title}' (confidence: {boundary.confidence})")
        
        # Show chapters
        print("\n3. Chapter Details:")
        for i, chapter in enumerate(result['chapters']):
            print(f"\n   Chapter {i+1}:")
            print(f"   Number: {chapter.get('chapter_number')}")
            print(f"   Title: {chapter.get('title')}")
            print(f"   Words: {chapter.get('word_count')}")
            print(f"   Preview: {chapter['text'][:100]}...")
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        Path(temp_path).unlink()


if __name__ == "__main__":
    success = test_parsing()
    sys.exit(0 if success else 1)
