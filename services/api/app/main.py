"""Main application module for the Inequality App API."""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import strawberry
from strawberry.fastapi import GraphQLRouter

from app.config import Settings
from app.db.session import engine, init_db
from app.routes import api_router
from app.graphql.schema import schema

settings = Settings()

app = FastAPI(
    title="Inequality App API",
    description="API for financial data on politicians and billionaires",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Set up REST API routes
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    pass

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Inequality App API",
        "version": "0.1.0",
        "documentation": "/docs",
        "graphql": "/graphql",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"} 