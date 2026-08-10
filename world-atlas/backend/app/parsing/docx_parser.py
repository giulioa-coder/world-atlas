"""
DOCX file parser for manuscript ingestion.

Uses python-docx library to extract text from Word documents.
"""

from pathlib import Path
from typing import Tuple

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class DocxParser:
    """Parser for Microsoft Word (.docx) files."""
    
    SUPPORTED_EXTENSIONS = {'.docx'}
    
    @classmethod
    def parse(cls, file_path: str) -> Tuple[str, int]:
        """
        Parse a DOCX file and return its content.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Tuple of (text_content, word_count)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid DOCX file
            ImportError: If python-docx is not installed
        """
        if not DOCX_AVAILABLE:
            raise ImportError(
                "python-docx is not installed. "
                "Install it with: pip install python-docx"
            )
        
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Read DOCX file
        doc = Document(file_path)
        
        # Extract all paragraphs
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)
        
        # Join paragraphs with double newlines
        text = '\n\n'.join(paragraphs)
        
        # Count words
        word_count = len(text.split())
        
        return text, word_count
    
    @classmethod
    def validate(cls, file_path: str) -> bool:
        """Validate that a file is a readable DOCX file."""
        if not DOCX_AVAILABLE:
            return False
        
        try:
            _, _ = cls.parse(file_path)
            return True
        except Exception:
            return False
