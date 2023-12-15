from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
