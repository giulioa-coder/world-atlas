"""
Text file parser for manuscript ingestion.

Handles plain text (.txt) files with basic encoding detection.
"""

import chardet
from pathlib import Path
from typing import Optional, Tuple


class TextParser:
    """Parser for plain text files."""
    
    SUPPORTED_EXTENSIONS = {'.txt', '.text'}
    
    @classmethod
    def detect_encoding(cls, file_path: str) -> str:
        """Detect the encoding of a text file."""
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')
    
    @classmethod
    def parse(cls, file_path: str) -> Tuple[str, int]:
        """
        Parse a text file and return its content.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Tuple of (text_content, word_count)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid text file
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Detect encoding
        encoding = cls.detect_encoding(file_path)
        
        # Read file content
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            text = f.read()
        
        # Count words
        word_count = len(text.split())
        
        return text, word_count
    
    @classmethod
    def validate(cls, file_path: str) -> bool:
        """Validate that a file is a readable text file."""
        try:
            _, _ = cls.parse(file_path)
            return True
        except Exception:
            return False
