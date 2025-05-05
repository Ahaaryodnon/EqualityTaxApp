"""Person model representing politicians and billionaires."""
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, String, Enum as SQLEnum, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class PersonType(str, Enum):
    """Type of person in the system."""

    POLITICIAN = "politician"
    BILLIONAIRE = "billionaire"
    OTHER = "other"


class Person(BaseModel):
    """Person model representing politicians and billionaires.

    This model stores basic information about individuals tracked in the system,
    including politicians (MPs, etc.) and billionaires.
    """

    full_name = Column(String(255), nullable=False, index=True)
    type = Column(SQLEnum(PersonType), nullable=False, index=True)
    
    # Optional fields
    title = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    middle_names = Column(String(255), nullable=True)
    
    # Politicians
    constituency = Column(String(255), nullable=True, index=True)
    party = Column(String(100), nullable=True, index=True)
    parliament_id = Column(String(50), nullable=True, unique=True)
    is_current_mp = Column(Boolean, nullable=True, default=None)
    
    # Billionaires
    forbes_id = Column(String(50), nullable=True, unique=True)
    estimated_wealth = Column(Float, nullable=True)  # In GBP
    wealth_source = Column(String(255), nullable=True)
    
    # Common fields
    biography = Column(Text, nullable=True)
    photo_url = Column(String(255), nullable=True)
    
    # Relationships
    financial_interests = relationship("FinancialInterest", back_populates="person")
    properties = relationship("Property", back_populates="person")
    assets = relationship("Asset", back_populates="person")
    
    def __repr__(self) -> str:
        """String representation of the person.

        Returns:
            str: String representation
        """
        return f"<Person {self.full_name} ({self.type.value})>"
    
    @property
    def total_wealth(self) -> float:
        """Calculate total wealth based on assets and properties.

        Returns:
            float: Total wealth in GBP
        """
        # For billionaires, use estimated wealth if available
        if self.type == PersonType.BILLIONAIRE and self.estimated_wealth:
            return self.estimated_wealth
            
        # Otherwise calculate from assets
        asset_total = sum(asset.value for asset in self.assets if asset.value)
        property_total = sum(prop.estimated_value for prop in self.properties if prop.estimated_value)
        
        return asset_total + property_total
    
    @property
    def yearly_passive_income(self) -> float:
        """Calculate yearly passive income.

        Returns:
            float: Yearly passive income in GBP
        """
        return sum(
            interest.yearly_value 
            for interest in self.financial_interests 
            if interest.yearly_value
        )
    
    @property
    def wealth_tax_contribution(self) -> float:
        """Calculate hypothetical wealth tax contribution.

        Uses 1% of wealth above £2 million threshold.

        Returns:
            float: Yearly wealth tax in GBP
        """
        taxable_wealth = max(0, self.total_wealth - 2_000_000)
        return taxable_wealth * 0.01 