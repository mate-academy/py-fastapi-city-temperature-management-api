from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.orm import Session

from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
