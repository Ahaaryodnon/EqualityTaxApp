"""Items for Scrapy spiders."""
import datetime
from typing import Optional, List, Dict, Any

import scrapy


class PersonItem(scrapy.Item):
    """Item for person data."""

    full_name = scrapy.Field()
    type = scrapy.Field()  # politician, billionaire, other
    title = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    middle_names = scrapy.Field()
    
    # Politicians
    constituency = scrapy.Field()
    party = scrapy.Field()
    parliament_id = scrapy.Field()
    is_current_mp = scrapy.Field()
    
    # Billionaires
    forbes_id = scrapy.Field()
    estimated_wealth = scrapy.Field()
    wealth_source = scrapy.Field()
    
    # Common fields
    biography = scrapy.Field()
    photo_url = scrapy.Field()
    
    # Metadata
    source_url = scrapy.Field()
    scrape_date = scrapy.Field()


class FinancialInterestItem(scrapy.Item):
    """Item for financial interest data."""

    # Relationships
    person_name = scrapy.Field()  # Used for linking, will be replaced with ID
    company_name = scrapy.Field()  # Used for linking, will be replaced with ID
    
    # Interest details
    type = scrapy.Field()  # employment, directorship, shareholding, etc.
    description = scrapy.Field()
    
    # Financial values
    amount = scrapy.Field()  # One-time amount
    yearly_value = scrapy.Field()  # Annualized value
    currency = scrapy.Field()
    
    # Dates
    registered_date = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    
    # Source information
    source_document = scrapy.Field()
    source_url = scrapy.Field()
    scrape_date = scrapy.Field()


class CompanyItem(scrapy.Item):
    """Item for company data."""

    name = scrapy.Field()
    
    # Company identifiers
    companies_house_id = scrapy.Field()
    sec_cik = scrapy.Field()
    lei = scrapy.Field()
    
    # Company details
    description = scrapy.Field()
    sector = scrapy.Field()
    industry = scrapy.Field()
    website = scrapy.Field()
    
    # Address
    address = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    postcode = scrapy.Field()
    
    # Financial data
    market_cap = scrapy.Field()
    annual_revenue = scrapy.Field()
    employee_count = scrapy.Field()
    
    # Public/private status
    is_public = scrapy.Field()
    stock_symbol = scrapy.Field()
    stock_exchange = scrapy.Field()
    
    # Metadata
    source_url = scrapy.Field()
    scrape_date = scrapy.Field()


class PropertyItem(scrapy.Item):
    """Item for property data."""

    # Relationships
    person_name = scrapy.Field()  # Used for linking, will be replaced with ID
    
    # Property details
    type = scrapy.Field()  # residential, commercial, agricultural, etc.
    description = scrapy.Field()
    
    # Location
    address = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    country = scrapy.Field()
    postcode = scrapy.Field()
    
    # Land Registry data
    land_registry_title = scrapy.Field()
    land_registry_date = scrapy.Field()
    
    # Financial details
    purchase_price = scrapy.Field()
    purchase_date = scrapy.Field()
    estimated_value = scrapy.Field()
    valuation_date = scrapy.Field()
    yearly_rental_income = scrapy.Field()
    
    # Ownership details
    ownership_percentage = scrapy.Field()
    is_primary_residence = scrapy.Field()
    
    # Metadata
    source_url = scrapy.Field()
    scrape_date = scrapy.Field()


class AssetItem(scrapy.Item):
    """Item for asset data."""

    # Relationships
    person_name = scrapy.Field()  # Used for linking, will be replaced with ID
    
    # Asset details
    type = scrapy.Field()  # stock, bond, fund, etc.
    name = scrapy.Field()
    description = scrapy.Field()
    
    # Financial details
    value = scrapy.Field()
    valuation_date = scrapy.Field()
    acquisition_cost = scrapy.Field()
    acquisition_date = scrapy.Field()
    yearly_income = scrapy.Field()
    
    # Stock-specific fields
    ticker_symbol = scrapy.Field()
    stock_exchange = scrapy.Field()
    quantity = scrapy.Field()
    
    # Source information
    source_document = scrapy.Field()
    source_url = scrapy.Field()
    
    # Metadata
    scrape_date = scrapy.Field() 