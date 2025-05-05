"""Persons API routes."""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.person import Person, PersonType
from app.schemas.person import PersonResponse, PersonDetailResponse, PersonCreate, PersonUpdate

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/", response_model=List[PersonResponse])
async def get_persons(
    skip: int = 0,
    limit: int = 100,
    type: Optional[PersonType] = None,
    party: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get list of persons.

    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        type: Filter by person type
        party: Filter by political party
        db: Database session dependency

    Returns:
        List of persons
    """
    query = select(Person)
    
    # Apply filters if provided
    if type:
        query = query.filter(Person.type == type)
    if party:
        query = query.filter(Person.party == party)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{person_id}", response_model=PersonDetailResponse)
async def get_person(
    person_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed information about a specific person.

    Args:
        person_id: UUID of the person
        db: Database session dependency

    Returns:
        Detailed person information including financial interests,
        properties, and assets.
    """
    query = select(Person).filter(Person.id == person_id)
    result = await db.execute(query)
    person = result.scalar_one_or_none()
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    return person


@router.get("/search/", response_model=List[PersonResponse])
async def search_persons(
    q: str = Query(..., min_length=3),
    db: AsyncSession = Depends(get_db),
):
    """Search for persons by name.

    Args:
        q: Search query (minimum 3 characters)
        db: Database session dependency

    Returns:
        List of matching persons
    """
    search_term = f"%{q}%"
    query = select(Person).filter(Person.full_name.ilike(search_term))
    result = await db.execute(query)
    return result.scalars().all() 