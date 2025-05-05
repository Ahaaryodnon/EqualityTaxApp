"""Property model for real estate holdings."""
from enum import Enum
from typing import Optional

from sqlalchemy import Column, String, Enum as SQLEnum, Float, Text, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class PropertyType(str, Enum):
    """Type of property."""

    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    AGRICULTURAL = "agricultural"
    INDUSTRIAL = "industrial"
    MIXED = "mixed"
    OTHER = "other"


class Property(BaseModel):
    """Property model.
    
    Represents real estate holdings owned by persons in the system.
    """

    # Relationships
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"), nullable=False, index=True)
    person = relationship("Person", back_populates="properties")
    
    # Property details
    type = Column(SQLEnum(PropertyType), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Location
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    county = Column(String(100), nullable=True, index=True)
    country = Column(String(100), nullable=True, index=True)
    postcode = Column(String(20), nullable=True)
    
    # Land Registry data
    land_registry_title = Column(String(100), nullable=True)
    land_registry_date = Column(Date, nullable=True)
    
    # Financial details
    purchase_price = Column(Float, nullable=True)  # In GBP
    purchase_date = Column(Date, nullable=True)
    estimated_value = Column(Float, nullable=True)  # In GBP
    valuation_date = Column(Date, nullable=True)
    yearly_rental_income = Column(Float, nullable=True)  # In GBP
    
    # Ownership details
    ownership_percentage = Column(Float, nullable=True, default=100.0)  # 0-100
    is_primary_residence = Column(Boolean, nullable=True, default=False)
    
    # Additional data
    metadata = Column(JSONB, nullable=True)
    
    def __repr__(self) -> str:
        """String representation of the property.

        Returns:
            str: String representation
        """
        location = self.city or self.county or self.country or "Unknown location"
        return f"<Property {self.type.value} in {location}>"
    
    @property
    def owned_value(self) -> float:
        """Calculate the value owned by the person based on ownership percentage.

        Returns:
            float: Owned value in GBP
        """
        if not self.estimated_value:
            return 0.0
        
        percentage = self.ownership_percentage or 100.0
        return (self.estimated_value * percentage) / 100.0 