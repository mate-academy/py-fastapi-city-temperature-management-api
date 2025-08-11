from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()



