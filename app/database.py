"""Async SQLAlchemy database configuration."""

from collections.abc import AsyncGenerator
import os

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./city_temperature.db",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"timeout": 20} if DATABASE_URL.startswith("sqlite") else {},
)

if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine.sync_engine, "connect")
    def enable_sqlite_foreign_keys(connection, _record) -> None:
        """Enable ON DELETE CASCADE for SQLite connections."""
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for ORM models."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for one request."""
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    """Create tables when the application starts."""
    # Import models so their table metadata is registered before create_all.
    from app import models  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

