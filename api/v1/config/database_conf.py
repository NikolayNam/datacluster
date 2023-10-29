from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
import logging

# Logging setup
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Get database connection credentials from environment variables
USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
HOST = os.environ.get("DB_HOST")
NAME = os.environ.get("DB_NAME")

# Construct the database URL using the credentials
DATABASE_URL = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}/{NAME}"

# Create an async engine with the database URL
engine = create_async_engine(
    DATABASE_URL, echo=True, isolation_level="REPEATABLE READ",
    pool_size=10, max_overflow=20)

# Configure a sessionmaker to create AsyncSession instances
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)

# Define an asynchronous context manager to provide database sessions


async def get_db():
    async with SessionLocal() as session:
        try:
            # Yield the session to the caller
            yield session
            # Commit the transaction after the caller is done using the session
            await session.commit()
        finally:
            # Close the session when the context manager exits
            await session.close()


class Base(DeclarativeBase):
    pass
# Define the Base class for all ORM models (legacy version)
# Base = declarative_base(cls=Base)

# SQLAlchemy 2.0.10 class Base (Currently version)
# class Base(DeclarativeBase):
#     pass
