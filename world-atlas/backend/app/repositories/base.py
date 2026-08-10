"""
Base repository with common CRUD operations.
"""

from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class Repository(Generic[ModelType]):
    """Base repository with generic CRUD operations."""
    
    def __init__(self, model: type[ModelType], db: Session):
        self.db = db
        self.model = model
    
    def get(self, id: UUID) -> Optional[ModelType]:
        """Get a single record by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """List records with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, id: UUID, **kwargs) -> Optional[ModelType]:
        """Update an existing record."""
        obj = self.get(id)
        if not obj:
            return None
        
        for field, value in kwargs.items():
            setattr(obj, field, value)
        
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: UUID) -> bool:
        """Delete a record by ID."""
        obj = self.get(id)
        if not obj:
            return False
        
        self.db.delete(obj)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Count total records."""
        return self.db.query(self.model).count()
