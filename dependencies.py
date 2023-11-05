from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db_session() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
