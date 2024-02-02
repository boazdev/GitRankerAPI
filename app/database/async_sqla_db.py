from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings.config import get_settings

# Use create_async_engine for asynchronous database connection.
engine = create_async_engine(get_settings().db_url, echo=True)

# Configure sessionmaker to use AsyncSession
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

# Define get_db as an async generator
async def get_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
