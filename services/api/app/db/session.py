"""SQLAlchemy session and engine setup."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import Settings

settings = Settings()

# PostgreSQL database URL with asyncpg driver
# Convert standard psycopg URL to asyncpg URL
db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Create declarative base for models
Base = declarative_base()


async def init_db() -> None:
    """Initialize the database, creating all tables.

    This should be called on application startup.
    """
    # Only create tables in development mode
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency for database session.

    Yields:
        AsyncSession: SQLAlchemy async session

    Example:
        ```python
        @app.get("/items/")
        async def get_items(db: AsyncSession = Depends(get_db)):
            items = await db.execute(select(Item))
            return items.scalars().all()
        ```
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 