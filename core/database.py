from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.settings import settings

engine = create_async_engine(
    url=settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Dependency that provides an async database session."""
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""

    pass
