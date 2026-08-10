"""
Chapter detection module.

Identifies chapter boundaries in manuscript text using pattern matching
and heuristics.
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ChapterBoundary:
    """Represents a detected chapter boundary."""
    index: int  # Character index in the text
    chapter_number: Optional[int]
    title: Optional[str]
    confidence: float  # 0.0-1.0
    pattern_type: str  # 'numbered', 'named', 'pattern'


class ChapterDetector:
    """Detects chapter boundaries in manuscript text."""
    
    # Common chapter patterns
    PATTERNS = [
        # "Chapter 1", "Chapter One", "Chapter I"
        (r'(?:^|\n)\s*(?:chapter|chap\.?|ch\.?)\s+(\d+|[IVXLC]+|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty))\s*(?:[:.-]\s*(.+))?\n', 'numbered'),
        
        # "Part I", "Book One"
        (r'(?:^|\n)\s*(?:part|book|section)\s+(\d+|[IVXLC]+)\s*(?:[:.-]\s*(.+))?\n', 'numbered'),
        
        # Numbered only: "1.", "1 -", "1:"
        (r'(?:^|\n)\s*(\d+)\s*[:.\-–—]\s+(.+)\n', 'numbered'),
        
        # Roman numerals alone
        (r'(?:^|\n)\s*([IVXLC]{1,5})\s*\n\s*(.+)\n', 'numbered'),
        
        # "The Beginning", "Prologue", "Epilogue"
        (r'(?:^|\n)\s*(prologue|epilogue|preface|introduction|conclusion|interlude)\s*(?:[:.-]\s*(.+))?\n', 'named'),
    ]
    
    def __init__(self, min_chapter_length: int = 500):
        """
        Initialize the chapter detector.
        
        Args:
            min_chapter_length: Minimum characters for a valid chapter
        """
        self.min_chapter_length = min_chapter_length
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE | re.MULTILINE), name)
            for pattern, name in self.PATTERNS
        ]
    
    def detect(self, text: str) -> List[ChapterBoundary]:
        """
        Detect chapter boundaries in text.
        
        Args:
            text: Full manuscript text
            
        Returns:
            List of ChapterBoundary objects, sorted by index
        """
        boundaries = []
        
        # Add start of document as first boundary
        boundaries.append(ChapterBoundary(
            index=0,
            chapter_number=0,
            title="Beginning",
            confidence=1.0,
            pattern_type='start'
        ))
        
        # Search for each pattern
        for pattern, pattern_type in self.compiled_patterns:
            for match in pattern.finditer(text):
                chapter_num_str = match.group(1)
                title = match.group(2).strip() if match.lastindex >= 2 and match.group(2) else None
                
                # Convert chapter number
                chapter_num = self._parse_chapter_number(chapter_num_str)
                
                # Calculate confidence based on pattern type
                confidence = self._calculate_confidence(pattern_type, match)
                
                boundaries.append(ChapterBoundary(
                    index=match.start(),
                    chapter_number=chapter_num,
                    title=title,
                    confidence=confidence,
                    pattern_type=pattern_type
                ))
        
        # Sort by index
        boundaries.sort(key=lambda b: b.index)
        
        # Remove duplicates (same position detected by multiple patterns)
        boundaries = self._deduplicate_boundaries(boundaries)
        
        return boundaries
    
    def split_into_chapters(self, text: str) -> List[Dict]:
        """
        Split text into chapters based on detected boundaries.
        
        Args:
            text: Full manuscript text
            
        Returns:
            List of chapter dictionaries with keys:
            - chapter_number
            - title
            - text
            - start_index
            - end_index
            - word_count
        """
        boundaries = self.detect(text)
        chapters = []
        
        for i, boundary in enumerate(boundaries):
            start_idx = boundary.index
            end_idx = boundaries[i + 1].index if i + 1 < len(boundaries) else len(text)
            
            chapter_text = text[start_idx:end_idx].strip()
            
            # Skip very short chapters (likely false positives)
            if len(chapter_text) < self.min_chapter_length:
                continue
            
            chapters.append({
                'chapter_number': boundary.chapter_number if boundary.chapter_number > 0 else None,
                'title': boundary.title,
                'text': chapter_text,
                'start_index': start_idx,
                'end_index': end_idx,
                'word_count': len(chapter_text.split()),
            })
        
        return chapters
    
    def _parse_chapter_number(self, num_str: str) -> int:
        """Convert chapter number string to integer."""
        if not num_str:
            return 0
        
        num_str = num_str.strip().lower()
        
        # Try Arabic numerals
        try:
            return int(num_str)
        except ValueError:
            pass
        
        # Roman numerals
        roman_map = {
            'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5,
            'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10,
            'xi': 11, 'xii': 12, 'xiii': 13, 'xiv': 14, 'xv': 15,
            'xx': 20, 'xxx': 30, 'xl': 40, 'l': 50, 'c': 100,
        }
        
        if num_str in roman_map:
            return roman_map[num_str]
        
        # Word numbers
        word_map = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
            'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
            'nineteen': 19, 'twenty': 20,
        }
        
        return word_map.get(num_str, 0)
    
    def _calculate_confidence(self, pattern_type: str, match) -> float:
        """Calculate confidence score for a detected boundary."""
        base_confidence = {
            'numbered': 0.9,
            'named': 0.8,
            'pattern': 0.6,
            'start': 1.0,
        }.get(pattern_type, 0.5)
        
        # Boost confidence if there's a title
        if match.lastindex >= 2 and match.group(2):
            base_confidence = min(base_confidence + 0.1, 1.0)
        
        return base_confidence
    
    def _deduplicate_boundaries(self, boundaries: List[ChapterBoundary]) -> List[ChapterBoundary]:
        """Remove duplicate boundaries at the same position."""
        if not boundaries:
            return []
        
        deduped = [boundaries[0]]
        
        for boundary in boundaries[1:]:
            # Keep if significantly different from last boundary
            if boundary.index - deduped[-1].index > 10:
                deduped.append(boundary)
            # Or if it has higher confidence
            elif boundary.confidence > deduped[-1].confidence:
                deduped[-1] = boundary
        
        return deduped
