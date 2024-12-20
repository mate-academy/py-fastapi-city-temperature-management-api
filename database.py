from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncAttrs
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    pass
