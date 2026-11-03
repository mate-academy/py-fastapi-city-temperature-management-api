
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from settings import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()
