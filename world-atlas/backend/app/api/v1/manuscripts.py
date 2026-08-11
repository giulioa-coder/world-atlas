"""
Manuscripts API router.

Handles manuscript upload, processing, and retrieval.
"""

import os
from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.exceptions import NotFoundException
from app.services.manuscript_service import ManuscriptService
from app.schemas.manuscript import (
    ManuscriptResponse,
    ManuscriptCreate,
    ChapterResponse,
    ProcessingResult,
)


router = APIRouter()


@router.post("/worlds/{world_id}/manuscripts/upload", response_model=ManuscriptResponse, status_code=201)
async def upload_manuscript(
    world_id: UUID,
    title: Optional[str] = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a manuscript for processing.
    
    Supported formats: TXT, DOCX, PDF
    
    The manuscript will be parsed and chapters will be automatically detected.
    """
    # Validate file type
    if not file.filename or '.' not in file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext not in ['txt', 'docx', 'pdf']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Supported: txt, docx, pdf"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size (max 50MB)
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 50MB"
        )
    
    # Create service and upload
    service = ManuscriptService(db)
    
    try:
        manuscript = service.upload_file(
            world_id=world_id,
            file_content=content,
            filename=file.filename,
            title=title,
        )
        
        return ManuscriptResponse.model_validate(manuscript)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/worlds/{world_id}/manuscripts/", response_model=List[ManuscriptResponse])
async def get_manuscripts_by_world(
    world_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all manuscripts for a world."""
    service = ManuscriptService(db)
    manuscripts = service.get_manuscripts_by_world(world_id)
    
    return [ManuscriptResponse.model_validate(m) for m in manuscripts]


@router.get("/manuscripts/{manuscript_id}", response_model=ManuscriptResponse)
async def get_manuscript(
    manuscript_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a manuscript by ID."""
    service = ManuscriptService(db)
    manuscript = service.get_manuscript(manuscript_id)
    
    if not manuscript:
        raise NotFoundException("Manuscript", manuscript_id)
    
    return ManuscriptResponse.model_validate(manuscript)


@router.post("/manuscripts/{manuscript_id}/process", response_model=ProcessingResult)
async def process_manuscript(
    manuscript_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Process a manuscript: parse text and detect chapters.
    
    This can take some time for large manuscripts, so it runs in the background.
    Use GET /{manuscript_id} to check the status.
    """
    service = ManuscriptService(db)
    manuscript = service.get_manuscript(manuscript_id)
    
    if not manuscript:
        raise NotFoundException("Manuscript", manuscript_id)
    
    # Process in background
    def process_task():
        try:
            result = service.process_manuscript(manuscript_id)
            print(f"Manuscript {manuscript_id} processed successfully: {result}")
        except Exception as e:
            print(f"Error processing manuscript {manuscript_id}: {e}")
    
    background_tasks.add_task(process_task)
    
    return ProcessingResult(
        manuscript_id=str(manuscript_id),
        status="processing",
        message="Manuscript processing started. Check status later."
    )


@router.get("/manuscripts/{manuscript_id}/chapters", response_model=List[ChapterResponse])
async def get_chapters(
    manuscript_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all chapters for a manuscript."""
    service = ManuscriptService(db)
    manuscript = service.get_manuscript(manuscript_id)
    
    if not manuscript:
        raise NotFoundException("Manuscript", manuscript_id)
    
    chapters = service.get_chapters(manuscript_id)
    
    return [ChapterResponse.model_validate(c) for c in chapters]


@router.get("/manuscripts/{manuscript_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    manuscript_id: UUID,
    chapter_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific chapter."""
    service = ManuscriptService(db)
    chapter = service.get_chapter(chapter_id)
    
    if not chapter or chapter.manuscript_id != manuscript_id:
        raise NotFoundException("Chapter", chapter_id)
    
    return ChapterResponse.model_validate(chapter)


@router.delete("/manuscripts/{manuscript_id}")
async def delete_manuscript(
    manuscript_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a manuscript and all its chapters."""
    service = ManuscriptService(db)
    success = service.delete_manuscript(manuscript_id)
    
    if not success:
        raise NotFoundException("Manuscript", manuscript_id)
    
    return {"message": "Manuscript deleted successfully"}

