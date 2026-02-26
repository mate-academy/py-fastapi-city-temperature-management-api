from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


# async context manager handles the close() automatically
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
