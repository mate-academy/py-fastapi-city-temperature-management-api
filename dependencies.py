from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db_session() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
