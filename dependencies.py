from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
