import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DB_URL")

# Create synchronous engine for Alembic
sync_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create asynchronous engine for FastAPI
async_engine = create_async_engine(
    DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),  # Use aiosqlite
    connect_args={"check_same_thread": False},
)

# Create synchronous session for Alembic
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Create asynchronous session for FastAPI
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()
