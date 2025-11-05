from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncAttrs
    )
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends


sqlalchemy_file_name = "weather_catalog.db"
sqlalchemy_database_url = f"sqlite+aiosqlite:///./{sqlalchemy_file_name}"

engine = create_async_engine(sqlalchemy_database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
    )


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
