"""Financial interest model representing passive income sources."""
from enum import Enum
from datetime import date
from typing import Optional

from sqlalchemy import Column, String, Enum as SQLEnum, Float, Text, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class InterestType(str, Enum):
    """Type of financial interest."""

    EMPLOYMENT = "employment"
    DIRECTORSHIP = "directorship"
    SHAREHOLDING = "shareholding"
    DONATION = "donation"
    GIFT = "gift"
    PROPERTY = "property"
    MISCELLANEOUS = "miscellaneous"


class FinancialInterest(BaseModel):
    """Financial interest model.
    
    Represents declared financial interests of persons in the system,
    such as employment, directorships, shareholdings, etc.
    """

    # Relationships
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"), nullable=False, index=True)
    person = relationship("Person", back_populates="financial_interests")
    
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=True)
    company = relationship("Company", back_populates="financial_interests")
    
    # Interest details
    type = Column(SQLEnum(InterestType), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Financial values
    amount = Column(Float, nullable=True)  # One-time amount
    yearly_value = Column(Float, nullable=True)  # Annualized value
    currency = Column(String(3), nullable=True, default="GBP")
    
    # Dates
    registered_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Source information
    source_document = Column(String(255), nullable=True)
    source_url = Column(String(255), nullable=True)
    is_verified = Column(Boolean, nullable=True, default=False)
    
    def __repr__(self) -> str:
        """String representation of the financial interest.

        Returns:
            str: String representation
        """
        return f"<FinancialInterest {self.type.value} for {self.person.full_name}>"
    
    @property
    def is_active(self) -> bool:
        """Check if the financial interest is currently active.

        Returns:
            bool: True if active, False otherwise
        """
        today = date.today()
        # If no end date, assume it's active
        if not self.end_date:
            return True
        return self.end_date >= today 