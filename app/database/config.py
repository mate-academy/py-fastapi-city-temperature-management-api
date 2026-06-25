from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

DATABASE_URL = "sqlite+aiosqlite:///main.db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


AsyncDatabaseSession = Annotated[AsyncSession, Depends(get_session)]
