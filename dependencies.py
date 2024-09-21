from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def pagination_parameters(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}
