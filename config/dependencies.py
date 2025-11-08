from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
