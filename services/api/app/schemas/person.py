"""Pydantic schemas for Person-related models."""
from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.person import PersonType


class PersonBase(BaseModel):
    """Base schema for Person data."""

    full_name: str
    type: PersonType
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_names: Optional[str] = None
    constituency: Optional[str] = None
    party: Optional[str] = None
    biography: Optional[str] = None
    photo_url: Optional[str] = None
    
    # Fields specific to politicians
    parliament_id: Optional[str] = None
    is_current_mp: Optional[bool] = None
    
    # Fields specific to billionaires
    forbes_id: Optional[str] = None
    estimated_wealth: Optional[float] = None
    wealth_source: Optional[str] = None


class PersonCreate(PersonBase):
    """Schema for creating a new Person."""

    pass


class PersonUpdate(BaseModel):
    """Schema for updating an existing Person.

    All fields are optional for updates.
    """

    full_name: Optional[str] = None
    type: Optional[PersonType] = None
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_names: Optional[str] = None
    constituency: Optional[str] = None
    party: Optional[str] = None
    biography: Optional[str] = None
    photo_url: Optional[str] = None
    parliament_id: Optional[str] = None
    is_current_mp: Optional[bool] = None
    forbes_id: Optional[str] = None
    estimated_wealth: Optional[float] = None
    wealth_source: Optional[str] = None


class FinancialInterestResponse(BaseModel):
    """Schema for financial interest response."""

    id: UUID
    type: str
    description: Optional[str] = None
    yearly_value: Optional[float] = None
    currency: Optional[str] = Field(default="GBP")
    registered_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_verified: Optional[bool] = False
    company_name: Optional[str] = None

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True


class PropertyResponse(BaseModel):
    """Schema for property response."""

    id: UUID
    type: str
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    estimated_value: Optional[float] = None
    yearly_rental_income: Optional[float] = None
    ownership_percentage: Optional[float] = Field(default=100.0)
    is_primary_residence: Optional[bool] = False

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True


class AssetResponse(BaseModel):
    """Schema for asset response."""

    id: UUID
    type: str
    name: str
    description: Optional[str] = None
    value: Optional[float] = None
    yearly_income: Optional[float] = None
    ticker_symbol: Optional[str] = None
    stock_exchange: Optional[str] = None

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True


class PersonResponse(PersonBase):
    """Schema for basic person response."""

    id: UUID
    created_at: date
    updated_at: date
    yearly_passive_income: float
    wealth_tax_contribution: float

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True


class PersonDetailResponse(PersonResponse):
    """Schema for detailed person response including related data."""

    financial_interests: List[FinancialInterestResponse] = []
    properties: List[PropertyResponse] = []
    assets: List[AssetResponse] = []

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True 