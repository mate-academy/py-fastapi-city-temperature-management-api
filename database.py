from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./cities_temperatures.db"
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./cities_temperatures.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()
