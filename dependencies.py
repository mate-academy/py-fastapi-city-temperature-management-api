from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def common_parameters(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}
