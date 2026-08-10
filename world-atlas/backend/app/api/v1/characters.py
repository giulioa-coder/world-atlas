"""
Characters API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.world import World
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterResponse


router = APIRouter()


@router.post("/worlds/{world_id}/", response_model=CharacterResponse, status_code=201)
def create_character(
    world_id: UUID,
    schema: CharacterCreate,
    db: Session = Depends(get_db),
):
    """Create a new character in a world."""
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("World", world_id)
    
    character = Character(
        world_id=world_id,
        name=schema.name,
        description=schema.description,
        role=schema.role,
    )
    db.add(character)
    db.commit()
    db.refresh(character)
    return CharacterResponse.model_validate(character)


@router.get("/worlds/{world_id}/", response_model=list[CharacterResponse])
def list_characters(
    world_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List all characters in a world."""
    characters = (
        db.query(Character)
        .filter(Character.world_id == world_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [CharacterResponse.model_validate(c) for c in characters]
