from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_session() -> AsyncSession:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        await db_session.close()
