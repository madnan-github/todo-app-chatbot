from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text
from src.config import settings

# Create async engine for Neon PostgreSQL
# Ensure the URL starts with postgresql+asyncpg://
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    database_url,
    echo=settings.environment == "development",
    future=True,
)

# Async session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables."""
    # Import models here to ensure they're registered with SQLModel.metadata
    from src.models import User, Task, Tag, TaskTag

    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Dependency for getting async database sessions."""
    async with async_session_maker() as session:
        yield session
