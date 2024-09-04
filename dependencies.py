from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
