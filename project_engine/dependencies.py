from sqlalchemy.ext.asyncio import AsyncSession

from project_engine.database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
