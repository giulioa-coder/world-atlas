"""
Characters API router.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.world import World
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate, CharacterResponse, CharacterListResponse
from app.core.exceptions import NotFoundException


router = APIRouter()


def get_character_service(db: Session = Depends(get_db)):
    """Simple character service helper."""
    return db


@router.post("/worlds/{world_id}/characters/", response_model=CharacterResponse, status_code=201)
def create_character(
    world_id: UUID,
    schema: CharacterCreate,
    db: Session = Depends(get_db),
):
    """Create a new character in a world."""
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
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


@router.get("/worlds/{world_id}/characters/", response_model=CharacterListResponse)
def list_characters(
    world_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List all characters in a world."""
    # Verify world exists
    world = db.get(World, world_id)
    if not world:
        raise NotFoundException("World", world_id)
    
    characters = (
        db.query(Character)
        .filter(Character.world_id == world_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    total = db.query(Character).filter(Character.world_id == world_id).count()
    return CharacterListResponse(items=[CharacterResponse.model_validate(c) for c in characters], total=total)


@router.get("/worlds/{world_id}/characters/search", response_model=CharacterListResponse)
def search_characters(
    world_id: UUID,
    q: str = Query(..., min_length=1, description="Search query for character name/description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Search characters in a world by name or description (case-insensitive)."""
    # Verify world exists
    world = db.get(World, world_id)
    if not world:
        raise NotFoundException("World", world_id)
    
    search_pattern = f"%{q}%"
    query = db.query(Character).filter(
        Character.world_id == world_id,
        (Character.name.ilike(search_pattern)) | (Character.description.ilike(search_pattern))
    )
    total = query.count()
    characters = query.offset(skip).limit(limit).all()
    
    return CharacterListResponse(items=[CharacterResponse.model_validate(c) for c in characters], total=total)


@router.get("/worlds/{world_id}/characters/{character_id}", response_model=CharacterResponse)
def get_character(
    world_id: UUID,
    character_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific character by ID."""
    # Verify world exists
    world = db.get(World, world_id)
    if not world:
        raise NotFoundException("World", world_id)
    
    character = db.get(Character, character_id)
    if not character:
        raise NotFoundException("Character", character_id)
    if character.world_id != world_id:
        raise NotFoundException("Character", character_id)
    
    return CharacterResponse.model_validate(character)


@router.put("/worlds/{world_id}/characters/{character_id}", response_model=CharacterResponse)
def update_character(
    world_id: UUID,
    character_id: UUID,
    schema: CharacterUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing character."""
    # Verify world exists
    world = db.get(World, world_id)
    if not world:
        raise NotFoundException("World", world_id)
    
    character = db.get(Character, character_id)
    if not character:
        raise NotFoundException("Character", character_id)
    if character.world_id != world_id:
        raise NotFoundException("Character", character_id)
    
    update_data = schema.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(character, field, value)
    
    db.commit()
    db.refresh(character)
    return CharacterResponse.model_validate(character)


@router.delete("/worlds/{world_id}/characters/{character_id}", status_code=204)
def delete_character(
    world_id: UUID,
    character_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a character."""
    # Verify world exists
    world = db.get(World, world_id)
    if not world:
        raise NotFoundException("World", world_id)
    
    character = db.get(Character, character_id)
    if not character:
        raise NotFoundException("Character", character_id)
    if character.world_id != world_id:
        raise NotFoundException("Character", character_id)
    
    db.delete(character)
    db.commit()
    return None
