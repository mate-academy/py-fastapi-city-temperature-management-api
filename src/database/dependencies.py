from sqlalchemy.ext.asyncio import AsyncSession

from src.database.engine import SessionLocal


# async def get_db() -> AsyncSession:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         await db.close()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session