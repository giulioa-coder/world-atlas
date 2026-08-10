"""
Parsing module for manuscript ingestion.

Provides a unified interface for parsing different file formats.
"""

from pathlib import Path
from typing import Tuple, Optional
from enum import Enum

from .txt_parser import TextParser
from .docx_parser import DocxParser
from .pdf_parser import PdfParser
from .chapter_detector import ChapterDetector


class FileType(str, Enum):
    """Supported file types."""
    TXT = "txt"
    DOCX = "docx"
    PDF = "pdf"


class ManuscriptParser:
    """
    Unified parser for manuscript files.
    
    Automatically detects file type and uses appropriate parser.
    """
    
    PARSERS = {
        FileType.TXT: TextParser,
        FileType.DOCX: DocxParser,
        FileType.PDF: PdfParser,
    }
    
    def __init__(self, min_chapter_length: int = 500):
        """
        Initialize the manuscript parser.
        
        Args:
            min_chapter_length: Minimum characters for a valid chapter
        """
        self.chapter_detector = ChapterDetector(min_chapter_length=min_chapter_length)
    
    @classmethod
    def detect_file_type(cls, file_path: str) -> FileType:
        """Detect file type from extension."""
        path = Path(file_path)
        suffix = path.suffix.lower().lstrip('.')
        
        if suffix in ['txt', 'text']:
            return FileType.TXT
        elif suffix == 'docx':
            return FileType.DOCX
        elif suffix == 'pdf':
            return FileType.PDF
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
    
    @classmethod
    def validate(cls, file_path: str) -> bool:
        """Validate that a file can be parsed."""
        try:
            file_type = cls.detect_file_type(file_path)
            parser = cls.PARSERS.get(file_type)
            
            if not parser:
                return False
            
            return parser.validate(file_path)
        except Exception:
            return False
    
    def parse(self, file_path: str) -> Tuple[str, int]:
        """
        Parse a manuscript file and return its content.
        
        Args:
            file_path: Path to the manuscript file
            
        Returns:
            Tuple of (text_content, word_count)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is not supported
            ImportError: If required parser library is not installed
        """
        file_type = self.detect_file_type(file_path)
        parser = self.PARSERS.get(file_type)
        
        if not parser:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return parser.parse(file_path)
    
    def parse_with_chapters(self, file_path: str) -> dict:
        """
        Parse a manuscript file and split into chapters.
        
        Args:
            file_path: Path to the manuscript file
            
        Returns:
            Dictionary with keys:
            - full_text: Complete manuscript text
            - word_count: Total word count
            - chapters: List of chapter dictionaries
            - chapter_count: Number of chapters detected
        """
        # Parse full text
        full_text, word_count = self.parse(file_path)
        
        # Split into chapters
        chapters = self.chapter_detector.split_into_chapters(full_text)
        
        return {
            'full_text': full_text,
            'word_count': word_count,
            'chapters': chapters,
            'chapter_count': len(chapters),
        }
