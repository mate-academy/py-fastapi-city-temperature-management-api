from sqlalchemy.orm import DeclarativeBase

from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
