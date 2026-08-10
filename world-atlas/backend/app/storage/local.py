"""
Local file storage implementation.

Stores files on the local filesystem with organization by world ID.
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from uuid import UUID

from app.core.config import settings


class LocalStorage:
    """Local filesystem storage backend."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize local storage.
        
        Args:
            base_path: Base directory for storage (defaults to settings.STORAGE_PATH)
        """
        self.base_path = Path(base_path or settings.STORAGE_PATH)
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """Ensure the base storage directory exists."""
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_world_directory(self, world_id: UUID) -> Path:
        """Get the directory for a specific world."""
        world_dir = self.base_path / str(world_id)
        world_dir.mkdir(parents=True, exist_ok=True)
        return world_dir
    
    def _get_manuscript_directory(self, world_id: UUID) -> Path:
        """Get the manuscript directory for a specific world."""
        manuscript_dir = self._get_world_directory(world_id) / "manuscripts"
        manuscript_dir.mkdir(parents=True, exist_ok=True)
        return manuscript_dir
    
    def save_manuscript(
        self,
        world_id: UUID,
        content: bytes,
        filename: str,
    ) -> str:
        """
        Save a manuscript file.
        
        Args:
            world_id: ID of the associated world
            content: Binary file content
            filename: Original filename
            
        Returns:
            Relative path to the saved file
        """
        import uuid
        
        # Create unique filename to avoid collisions
        file_ext = Path(filename).suffix.lower()
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Get directory
        manuscript_dir = self._get_manuscript_directory(world_id)
        
        # Full path
        file_path = manuscript_dir / unique_filename
        
        # Write file
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Return relative path (world_id/manuscripts/filename)
        return f"{world_id}/manuscripts/{unique_filename}"
    
    def get_full_path(self, relative_path: str) -> str:
        """
        Get the full filesystem path from a relative path.
        
        Args:
            relative_path: Relative path stored in database
            
        Returns:
            Full filesystem path
        """
        full_path = self.base_path / relative_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")
        
        return str(full_path)
    
    def read_file(self, relative_path: str) -> bytes:
        """
        Read a file's contents.
        
        Args:
            relative_path: Relative path stored in database
            
        Returns:
            Binary file content
        """
        full_path = self.get_full_path(relative_path)
        
        with open(full_path, 'rb') as f:
            return f.read()
    
    def file_exists(self, relative_path: str) -> bool:
        """Check if a file exists."""
        full_path = self.base_path / relative_path
        return full_path.exists()
    
    def delete_file(self, relative_path: str) -> bool:
        """
        Delete a file.
        
        Args:
            relative_path: Relative path stored in database
            
        Returns:
            True if deleted successfully
        """
        try:
            full_path = self.get_full_path(relative_path)
            os.remove(full_path)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    def get_file_size(self, relative_path: str) -> int:
        """Get file size in bytes."""
        full_path = self.get_full_path(relative_path)
        return os.path.getsize(full_path)
    
    def cleanup_world(self, world_id: UUID) -> bool:
        """
        Delete all files for a world.
        
        Args:
            world_id: ID of the world
            
        Returns:
            True if cleanup successful
        """
        world_dir = self._get_world_directory(world_id)
        
        if world_dir.exists():
            shutil.rmtree(world_dir)
            return True
        
        return False
