from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncIterator[AsyncSession]:
    session = SessionLocal

    async with session() as db:
        try:
            yield db
        finally:
            await db.close()
