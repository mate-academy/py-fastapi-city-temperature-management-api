from typing import AsyncGenerator
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
