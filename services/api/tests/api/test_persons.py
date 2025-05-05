"""Tests for the persons API endpoints."""
import uuid
from typing import Dict, Any

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person, PersonType


async def create_test_person(db: AsyncSession, **kwargs) -> Person:
    """Create a test person in the database.

    Args:
        db: Database session
        **kwargs: Override default person values

    Returns:
        Created person instance
    """
    default_values = {
        "full_name": "Test Person",
        "type": PersonType.POLITICIAN,
        "title": "Mr",
        "first_name": "Test",
        "last_name": "Person",
        "constituency": "Test Constituency",
        "party": "Test Party",
        "parliament_id": f"MP{uuid.uuid4().hex[:8]}",
        "is_current_mp": True,
    }
    
    # Override defaults with provided values
    person_data = {**default_values, **kwargs}
    
    # Create person
    person = Person(**person_data)
    db.add(person)
    await db.commit()
    await db.refresh(person)
    
    return person


@pytest.mark.asyncio
async def test_get_persons_empty(client: AsyncClient):
    """Test GET /api/persons returns empty list when no persons exist."""
    response = await client.get("/api/persons")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_persons(client: AsyncClient, db_session: AsyncSession):
    """Test GET /api/persons returns list of persons."""
    # Create test persons
    person1 = await create_test_person(db_session, full_name="Alice Smith")
    person2 = await create_test_person(db_session, full_name="Bob Jones", type=PersonType.BILLIONAIRE)
    
    response = await client.get("/api/persons")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    # Check person data
    person_names = [p["full_name"] for p in data]
    assert "Alice Smith" in person_names
    assert "Bob Jones" in person_names


@pytest.mark.asyncio
async def test_get_person_by_id(client: AsyncClient, db_session: AsyncSession):
    """Test GET /api/persons/{id} returns person details."""
    person = await create_test_person(db_session, full_name="Charlie Brown")
    
    response = await client.get(f"/api/persons/{person.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["full_name"] == "Charlie Brown"
    assert data["type"] == "politician"
    assert data["constituency"] == "Test Constituency"
    assert data["party"] == "Test Party"
    
    # Check computed fields
    assert "yearly_passive_income" in data
    assert "wealth_tax_contribution" in data
    
    # Check related data
    assert "financial_interests" in data
    assert "properties" in data
    assert "assets" in data


@pytest.mark.asyncio
async def test_get_person_not_found(client: AsyncClient):
    """Test GET /api/persons/{id} returns 404 for non-existent person."""
    random_id = str(uuid.uuid4())
    response = await client.get(f"/api/persons/{random_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"


@pytest.mark.asyncio
async def test_search_persons(client: AsyncClient, db_session: AsyncSession):
    """Test GET /api/persons/search finds persons by name."""
    # Create test persons with different names
    await create_test_person(db_session, full_name="David Smith")
    await create_test_person(db_session, full_name="Emily Jones")
    await create_test_person(db_session, full_name="Frederick Smith")
    
    # Search for "Smith"
    response = await client.get("/api/persons/search/?q=Smith")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    # Check search results
    person_names = [p["full_name"] for p in data]
    assert "David Smith" in person_names
    assert "Frederick Smith" in person_names
    assert "Emily Jones" not in person_names 