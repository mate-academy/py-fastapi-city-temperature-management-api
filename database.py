from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = async_sessionmaker(async_engine)
# SessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, class_=AsyncSession, bind=async_engine
# )

Base = declarative_base()
