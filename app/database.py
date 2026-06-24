from collections.abc import AsyncGenerator
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connection_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    bind=engine,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
