"""Asset model for non-property holdings."""
from enum import Enum
from typing import Optional

from sqlalchemy import Column, String, Enum as SQLEnum, Float, Text, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class AssetType(str, Enum):
    """Type of asset."""

    STOCK = "stock"
    BOND = "bond"
    FUND = "fund"
    CRYPTO = "cryptocurrency"
    ARTWORK = "artwork"
    VEHICLE = "vehicle"
    JEWELRY = "jewelry"
    CASH = "cash"
    OTHER = "other"


class Asset(BaseModel):
    """Asset model.
    
    Represents non-property assets owned by persons in the system,
    such as stocks, bonds, artwork, etc.
    """

    # Relationships
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"), nullable=False, index=True)
    person = relationship("Person", back_populates="assets")
    
    # Asset details
    type = Column(SQLEnum(AssetType), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Financial details
    value = Column(Float, nullable=True)  # In GBP
    valuation_date = Column(Date, nullable=True)
    acquisition_cost = Column(Float, nullable=True)  # In GBP
    acquisition_date = Column(Date, nullable=True)
    yearly_income = Column(Float, nullable=True)  # In GBP
    
    # Stock-specific fields
    ticker_symbol = Column(String(20), nullable=True)
    stock_exchange = Column(String(50), nullable=True)
    quantity = Column(Float, nullable=True)
    
    # Source information
    source_document = Column(String(255), nullable=True)
    source_url = Column(String(255), nullable=True)
    is_verified = Column(Boolean, nullable=True, default=False)
    
    def __repr__(self) -> str:
        """String representation of the asset.

        Returns:
            str: String representation
        """
        return f"<Asset {self.type.value} - {self.name}>" 