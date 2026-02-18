from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import SQLALCHEMY_DATABASE_URI

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass
