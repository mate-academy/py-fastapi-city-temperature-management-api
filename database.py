from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import settings


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


# check_same_thread is not needed with async SQLite
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# async_sessionmaker already sets autocommit=False and autoflush=False
SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
