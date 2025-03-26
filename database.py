from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from models import Base

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./arithmetic.db")

# Create engine
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create session factory
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """Get database session"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database and create tables"""
    try:
        async with engine.begin() as conn:
            # Drop all tables first
            await conn.run_sync(Base.metadata.drop_all)
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise
