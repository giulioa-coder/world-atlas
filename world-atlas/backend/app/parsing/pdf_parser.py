"""
PDF file parser for manuscript ingestion.

Uses PyPDF2 library to extract text from PDF documents.
"""

from pathlib import Path
from typing import Tuple

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class PdfParser:
    """Parser for PDF files."""
    
    SUPPORTED_EXTENSIONS = {'.pdf'}
    
    @classmethod
    def parse(cls, file_path: str) -> Tuple[str, int]:
        """
        Parse a PDF file and return its content.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (text_content, word_count)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid PDF file
            ImportError: If PyPDF2 is not installed
        """
        if not PYPDF2_AVAILABLE:
            raise ImportError(
                "PyPDF2 is not installed. "
                "Install it with: pip install PyPDF2"
            )
        
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Read PDF file
        reader = PdfReader(file_path)
        
        # Extract all pages
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text)
        
        # Join pages with double newlines
        text = '\n\n'.join(pages)
        
        # Count words
        word_count = len(text.split())
        
        return text, word_count
    
    @classmethod
    def validate(cls, file_path: str) -> bool:
        """Validate that a file is a readable PDF file."""
        if not PYPDF2_AVAILABLE:
            return False
        
        try:
            _, _ = cls.parse(file_path)
            return True
        except Exception:
            return False
