from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool
from sqlalchemy import MetaData, Integer, Column

from src.config import settings


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


metadata = MetaData()


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL, poolclass=NullPool, echo=True
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
