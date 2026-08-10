"""
Manuscript service for handling file uploads and processing.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.manuscript import Manuscript, Chapter, ManuscriptStatus
from app.models.world import World
from app.parsing import ManuscriptParser
from app.storage.local import LocalStorage


class ManuscriptService:
    """Service for manuscript management and processing."""
    
    def __init__(self, db: Session, storage: Optional[LocalStorage] = None):
        """
        Initialize the manuscript service.
        
        Args:
            db: Database session
            storage: Storage backend (defaults to LocalStorage)
        """
        self.db = db
        self.storage = storage or LocalStorage()
        self.parser = ManuscriptParser()
    
    def create_manuscript(
        self,
        world_id: UUID,
        title: str,
        file_path: str,
        file_type: str,
    ) -> Manuscript:
        """
        Create a new manuscript record.
        
        Args:
            world_id: ID of the associated world
            title: Manuscript title
            file_path: Path to the uploaded file
            file_type: File type (txt, docx, pdf)
            
        Returns:
            Created Manuscript object
        """
        manuscript = Manuscript(
            world_id=world_id,
            title=title,
            file_path=file_path,
            file_type=file_type,
            status=ManuscriptStatus.PENDING,
        )
        
        self.db.add(manuscript)
        self.db.commit()
        self.db.refresh(manuscript)
        
        return manuscript
    
    def upload_file(
        self,
        world_id: UUID,
        file_content: bytes,
        filename: str,
        title: Optional[str] = None,
    ) -> Manuscript:
        """
        Upload a manuscript file and create a manuscript record.
        
        Args:
            world_id: ID of the associated world
            file_content: Binary file content
            filename: Original filename
            title: Optional title (defaults to filename without extension)
            
        Returns:
            Created Manuscript object
        """
        # Determine file type from extension
        file_type = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'txt'
        
        if file_type not in ['txt', 'docx', 'pdf']:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Generate storage path
        stored_path = self.storage.save_manuscript(world_id, file_content, filename)
        
        # Create title from filename if not provided
        if not title:
            title = Path(filename).stem
        
        # Create manuscript record
        manuscript = self.create_manuscript(
            world_id=world_id,
            title=title,
            file_path=stored_path,
            file_type=file_type,
        )
        
        return manuscript
    
    def process_manuscript(self, manuscript_id: UUID) -> dict:
        """
        Process a manuscript: parse text, detect chapters, create records.
        
        Args:
            manuscript_id: ID of the manuscript to process
            
        Returns:
            Processing result with statistics
            
        Raises:
            FileNotFoundError: If manuscript file doesn't exist
            ValueError: If manuscript cannot be parsed
        """
        manuscript = self.db.query(Manuscript).get(manuscript_id)
        
        if not manuscript:
            raise ValueError(f"Manuscript not found: {manuscript_id}")
        
        # Update status
        manuscript.status = ManuscriptStatus.PROCESSING
        self.db.commit()
        
        try:
            # Get full file path
            full_path = self.storage.get_full_path(manuscript.file_path)
            
            # Parse manuscript
            result = self.parser.parse_with_chapters(full_path)
            
            # Update manuscript with word count
            manuscript.word_count = result['word_count']
            
            # Create chapter records
            chapters_created = []
            for i, chapter_data in enumerate(result['chapters']):
                chapter = Chapter(
                    manuscript_id=manuscript_id,
                    chapter_number=chapter_data.get('chapter_number'),
                    title=chapter_data.get('title'),
                    text=chapter_data['text'],
                    word_count=chapter_data['word_count'],
                    chronological_order=i,
                    start_index=chapter_data.get('start_index', 0),
                    end_index=chapter_data.get('end_index', 0),
                )
                self.db.add(chapter)
                chapters_created.append(chapter)
            
            # Mark as completed
            manuscript.status = ManuscriptStatus.COMPLETED
            manuscript.processed_at = datetime.utcnow()
            
            self.db.commit()
            
            return {
                'status': 'completed',
                'word_count': result['word_count'],
                'chapter_count': len(chapters_created),
                'chapters': [
                    {
                        'id': str(ch.id),
                        'number': ch.chapter_number,
                        'title': ch.title,
                        'word_count': ch.word_count,
                    }
                    for ch in chapters_created
                ],
            }
            
        except Exception as e:
            # Mark as failed
            manuscript.status = ManuscriptStatus.FAILED
            manuscript.error_message = str(e)
            self.db.commit()
            
            raise
    
    def get_manuscript(self, manuscript_id: UUID) -> Optional[Manuscript]:
        """Get a manuscript by ID."""
        return self.db.query(Manuscript).filter(
            Manuscript.id == manuscript_id
        ).first()
    
    def get_manuscripts_by_world(self, world_id: UUID) -> List[Manuscript]:
        """Get all manuscripts for a world."""
        return self.db.query(Manuscript).filter(
            Manuscript.world_id == world_id
        ).all()
    
    def get_chapters(self, manuscript_id: UUID) -> List[Chapter]:
        """Get all chapters for a manuscript."""
        return self.db.query(Chapter).filter(
            Chapter.manuscript_id == manuscript_id
        ).order_by(Chapter.chronological_order).all()
    
    def get_chapter(self, chapter_id: UUID) -> Optional[Chapter]:
        """Get a chapter by ID."""
        return self.db.query(Chapter).get(chapter_id)
    
    def delete_manuscript(self, manuscript_id: UUID) -> bool:
        """
        Delete a manuscript and its chapters.
        
        Args:
            manuscript_id: ID of the manuscript to delete
            
        Returns:
            True if deleted successfully
        """
        manuscript = self.get_manuscript(manuscript_id)
        
        if not manuscript:
            return False
        
        # Delete associated file
        try:
            self.storage.delete_file(manuscript.file_path)
        except Exception:
            pass  # Continue even if file deletion fails
        
        # Delete manuscript (chapters will be deleted via cascade)
        self.db.delete(manuscript)
        self.db.commit()
        
        return True
