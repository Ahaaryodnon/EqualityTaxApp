"""API routes package."""
from fastapi import APIRouter

from app.routes.persons import router as persons_router
from app.routes.companies import router as companies_router
from app.routes.statistics import router as statistics_router

# Create main API router
api_router = APIRouter(prefix="/api")

# Include all route modules
api_router.include_router(persons_router)
api_router.include_router(companies_router)
api_router.include_router(statistics_router)

__all__ = ["api_router"] 