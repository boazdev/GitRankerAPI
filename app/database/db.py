""" from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings.config import get_settings

engine = create_engine(get_settings().db_url)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 """
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
    class_=AsyncSession,

)

Base = declarative_base()

# Define get_db as an async generator
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            async with session.begin():
                yield session
        except Exception as e:
            await session.rollback()  # Rollback on any unexpected errors
            raise e  # Re-raise the exception for proper handling
        finally:
            await session.close()  # Ensure session closure even if exceptions occur