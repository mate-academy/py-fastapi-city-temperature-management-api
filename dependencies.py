from sqlalchemy.ext.asyncio import AsyncSession

import database


async def get_db() -> AsyncSession:
    db = database.SessionLocal()

    try:
        yield db
    finally:
        await db.close()
