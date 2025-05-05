"""Company model for organizations related to financial interests."""
from typing import Optional, List

from sqlalchemy import Column, String, Text, Float, Boolean, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Company(BaseModel):
    """Company model.
    
    Represents companies, organizations, and other entities that are related
    to financial interests of persons in the system.
    """

    name = Column(String(255), nullable=False, index=True)
    
    # Company identifiers
    companies_house_id = Column(String(50), nullable=True, unique=True, index=True)
    sec_cik = Column(String(50), nullable=True, unique=True)  # SEC Central Index Key
    lei = Column(String(50), nullable=True, unique=True)  # Legal Entity Identifier
    
    # Company details
    description = Column(Text, nullable=True)
    sector = Column(String(100), nullable=True, index=True)
    industry = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True, index=True)
    postcode = Column(String(20), nullable=True)
    
    # Financial data
    market_cap = Column(Float, nullable=True)  # In GBP
    annual_revenue = Column(Float, nullable=True)  # In GBP
    employee_count = Column(Integer, nullable=True)
    
    # Public/private status
    is_public = Column(Boolean, nullable=True)
    stock_symbol = Column(String(20), nullable=True)
    stock_exchange = Column(String(50), nullable=True)
    
    # Relationships
    financial_interests = relationship("FinancialInterest", back_populates="company")
    
    def __repr__(self) -> str:
        """String representation of the company.

        Returns:
            str: String representation
        """
        return f"<Company {self.name}>" 