"""GraphQL schema for the Inequality App API."""
import uuid
from typing import List, Optional

import strawberry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from app.db.session import get_db
from app.models.person import Person as PersonModel, PersonType as PersonTypeModel
from app.models.financial_interest import FinancialInterest as FinancialInterestModel
from app.models.company import Company as CompanyModel
from app.models.property import Property as PropertyModel
from app.models.asset import Asset as AssetModel


@strawberry.enum
class PersonType:
    """GraphQL enum for person types."""

    POLITICIAN = "politician"
    BILLIONAIRE = "billionaire"
    OTHER = "other"


@strawberry.type
class FinancialInterest:
    """GraphQL type for financial interests."""

    id: strawberry.ID
    type: str
    description: Optional[str] = None
    yearly_value: Optional[float] = None
    currency: str = "GBP"
    company_name: Optional[str] = None


@strawberry.type
class Property:
    """GraphQL type for properties."""

    id: strawberry.ID
    type: str
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    estimated_value: Optional[float] = None
    yearly_rental_income: Optional[float] = None


@strawberry.type
class Asset:
    """GraphQL type for assets."""

    id: strawberry.ID
    type: str
    name: str
    description: Optional[str] = None
    value: Optional[float] = None
    yearly_income: Optional[float] = None


@strawberry.type
class Person:
    """GraphQL type for persons."""

    id: strawberry.ID
    full_name: str
    type: PersonType
    title: Optional[str] = None
    constituency: Optional[str] = None
    party: Optional[str] = None
    biography: Optional[str] = None
    photo_url: Optional[str] = None
    estimated_wealth: Optional[float] = None
    yearly_passive_income: float
    wealth_tax_contribution: float

    @strawberry.field
    async def financial_interests(self, info: Info) -> List[FinancialInterest]:
        """Resolve financial interests for the person.

        Args:
            info: GraphQL resolver info

        Returns:
            List of financial interests
        """
        db = info.context["db"]
        query = select(FinancialInterestModel).filter(FinancialInterestModel.person_id == uuid.UUID(self.id))
        result = await db.execute(query)
        models = result.scalars().all()
        
        interests = []
        for model in models:
            company_name = None
            if model.company:
                company_name = model.company.name
                
            interests.append(
                FinancialInterest(
                    id=str(model.id),
                    type=model.type.value,
                    description=model.description,
                    yearly_value=model.yearly_value,
                    currency=model.currency or "GBP",
                    company_name=company_name,
                )
            )
        
        return interests

    @strawberry.field
    async def properties(self, info: Info) -> List[Property]:
        """Resolve properties for the person.

        Args:
            info: GraphQL resolver info

        Returns:
            List of properties
        """
        db = info.context["db"]
        query = select(PropertyModel).filter(PropertyModel.person_id == uuid.UUID(self.id))
        result = await db.execute(query)
        models = result.scalars().all()
        
        return [
            Property(
                id=str(model.id),
                type=model.type.value,
                description=model.description,
                address=model.address,
                city=model.city,
                estimated_value=model.estimated_value,
                yearly_rental_income=model.yearly_rental_income,
            )
            for model in models
        ]

    @strawberry.field
    async def assets(self, info: Info) -> List[Asset]:
        """Resolve assets for the person.

        Args:
            info: GraphQL resolver info

        Returns:
            List of assets
        """
        db = info.context["db"]
        query = select(AssetModel).filter(AssetModel.person_id == uuid.UUID(self.id))
        result = await db.execute(query)
        models = result.scalars().all()
        
        return [
            Asset(
                id=str(model.id),
                type=model.type.value,
                name=model.name,
                description=model.description,
                value=model.value,
                yearly_income=model.yearly_income,
            )
            for model in models
        ]


@strawberry.type
class Query:
    """GraphQL root query type."""

    @strawberry.field
    async def persons(
        self, 
        info: Info, 
        type: Optional[PersonType] = None,
        party: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Person]:
        """Query to retrieve persons.

        Args:
            info: GraphQL resolver info
            type: Optional filter by person type
            party: Optional filter by political party
            limit: Pagination limit
            offset: Pagination offset

        Returns:
            List of persons
        """
        db = info.context["db"]
        query = select(PersonModel)
        
        # Apply filters
        if type:
            person_type = PersonTypeModel(type)
            query = query.filter(PersonModel.type == person_type)
            
        if party:
            query = query.filter(PersonModel.party == party)
            
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        result = await db.execute(query)
        models = result.scalars().all()
        
        return [
            Person(
                id=str(model.id),
                full_name=model.full_name,
                type=PersonType(model.type.value),
                title=model.title,
                constituency=model.constituency,
                party=model.party,
                biography=model.biography,
                photo_url=model.photo_url,
                estimated_wealth=model.estimated_wealth,
                yearly_passive_income=model.yearly_passive_income,
                wealth_tax_contribution=model.wealth_tax_contribution,
            )
            for model in models
        ]

    @strawberry.field
    async def person(self, info: Info, id: str) -> Optional[Person]:
        """Query to retrieve a specific person by ID.

        Args:
            info: GraphQL resolver info
            id: Person ID

        Returns:
            Person or None if not found
        """
        db = info.context["db"]
        query = select(PersonModel).filter(PersonModel.id == uuid.UUID(id))
        result = await db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
            
        return Person(
            id=str(model.id),
            full_name=model.full_name,
            type=PersonType(model.type.value),
            title=model.title,
            constituency=model.constituency,
            party=model.party,
            biography=model.biography,
            photo_url=model.photo_url,
            estimated_wealth=model.estimated_wealth,
            yearly_passive_income=model.yearly_passive_income,
            wealth_tax_contribution=model.wealth_tax_contribution,
        )


# Create schema
schema = strawberry.Schema(
    query=Query,
    config=strawberry.StrawberryConfig(
        auto_camel_case=True,
    ),
)


# Context dependency
async def get_context(db: AsyncSession = Depends(get_db)):
    """Create the GraphQL context.

    Args:
        db: Database session dependency

    Returns:
        GraphQL context
    """
    return {"db": db} 