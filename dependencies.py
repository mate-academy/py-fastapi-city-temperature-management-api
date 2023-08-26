from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def common_city_parameters(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    return {"db": db, "city_id": city_id}
