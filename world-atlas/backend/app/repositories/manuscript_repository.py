"""
Manuscript repository for database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.manuscript import Manuscript, ManuscriptStatus, Chapter
from app.repositories.base import Repository


class ManuscriptRepository(Repository[Manuscript]):
    """Repository for Manuscript model operations."""
    
    def __init__(self, db: Session):
        super().__init__(model=Manuscript, db=db)
    
    def get_by_world(self, world_id: UUID) -> List[Manuscript]:
        """Get all manuscripts for a specific world."""
        return self.db.query(Manuscript).filter(Manuscript.world_id == world_id).all()
    
    def get_by_status(self, status: ManuscriptStatus) -> List[Manuscript]:
        """Get manuscripts by processing status."""
        return self.db.query(Manuscript).filter(Manuscript.status == status).all()
    
    def get_by_world_and_status(
        self, 
        world_id: UUID, 
        status: ManuscriptStatus
    ) -> List[Manuscript]:
        """Get manuscripts for a specific world and status."""
        return self.db.query(Manuscript).filter(
            Manuscript.world_id == world_id,
            Manuscript.status == status
        ).all()
    
    def get_pending_processing(self) -> List[Manuscript]:
        """Get all manuscripts pending processing."""
        return self.db.query(Manuscript).filter(
            Manuscript.status == ManuscriptStatus.PENDING
        ).all()
    
    def get_failed(self) -> List[Manuscript]:
        """Get all failed manuscripts."""
        return self.db.query(Manuscript).filter(
            Manuscript.status == ManuscriptStatus.FAILED
        ).all()
    
    def update_status(
        self, 
        id: UUID, 
        status: ManuscriptStatus,
        error_message: Optional[str] = None
    ) -> Optional[Manuscript]:
        """Update manuscript processing status."""
        update_data = {"status": status}
        if error_message:
            update_data["error_message"] = error_message
        if status == ManuscriptStatus.COMPLETED:
            from datetime import datetime
            update_data["processed_at"] = datetime.utcnow()
        return self.update(id, **update_data)
    
    def get_with_chapters(self, id: UUID) -> Optional[Manuscript]:
        """Get manuscript with its chapters."""
        return (
            self.db.query(Manuscript)
            .filter(Manuscript.id == id)
            .first()
        )
    
    def count_by_world(self, world_id: UUID) -> int:
        """Count manuscripts for a specific world."""
        return self.db.query(Manuscript).filter(
            Manuscript.world_id == world_id
        ).count()


class ChapterRepository:
    """Repository for Chapter model operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.model = Chapter
    
    def get_by_manuscript(self, manuscript_id: UUID) -> List[Chapter]:
        """Get all chapters for a manuscript."""
        return self.db.query(Chapter).filter(
            Chapter.manuscript_id == manuscript_id
        ).order_by(Chapter.chapter_number).all()
    
    def get_by_id(self, chapter_id: UUID) -> Optional[Chapter]:
        """Get a chapter by ID."""
        return self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
    
    def create_chapter(self, **kwargs) -> Chapter:
        """Create a new chapter."""
        chapter = Chapter(**kwargs)
        self.db.add(chapter)
        self.db.commit()
        self.db.refresh(chapter)
        return chapter
    
    def update_chapter(self, chapter_id: UUID, **kwargs) -> Optional[Chapter]:
        """Update a chapter."""
        chapter = self.get_by_id(chapter_id)
        if not chapter:
            return None
        
        for field, value in kwargs.items():
            setattr(chapter, field, value)
        
        self.db.commit()
        self.db.refresh(chapter)
        return chapter
    
    def delete_chapter(self, chapter_id: UUID) -> bool:
        """Delete a chapter."""
        chapter = self.get_by_id(chapter_id)
        if not chapter:
            return False
        
        self.db.delete(chapter)
        self.db.commit()
        return True
    
    def count_by_manuscript(self, manuscript_id: UUID) -> int:
        """Count chapters for a manuscript."""
        return self.db.query(Chapter).filter(
            Chapter.manuscript_id == manuscript_id
        ).count()
