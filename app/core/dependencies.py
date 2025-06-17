from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal

async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
