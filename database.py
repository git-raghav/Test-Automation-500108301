from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from base import Base
from logger import logger

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./arithmetic.db")

# Create engine with proper error handling
try:
    # Configure engine based on database type
    if DATABASE_URL.startswith("postgresql"):
        engine = create_async_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Enable connection health checks
            pool_size=5,  # Set reasonable pool size
            max_overflow=10,  # Allow some overflow connections
            echo=True  # Enable SQL logging for debugging
        )
    else:
        engine = create_async_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=True  # Enable SQL logging for debugging
        )
    logger.info(f"Database engine created successfully for URL: {DATABASE_URL}")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create session factory with error handling
try:
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    logger.info("Session factory created successfully")
except Exception as e:
    logger.error(f"Failed to create session factory: {str(e)}")
    raise

async def get_db():
    """Get database session with error handling"""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database and create tables safely"""
    try:
        async with engine.begin() as conn:
            # Only create tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

async def drop_db():
    """Drop all tables (for testing only)"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {str(e)}")
        raise
