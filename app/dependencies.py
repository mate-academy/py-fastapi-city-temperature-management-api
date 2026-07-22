from typing import AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database import SessionLocal


async def get_db() -> AsyncGenerator:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def database_city_id_params(city_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return {"city_id": city_id, "db": db}


DatabaseCityIdParams = Annotated[dict, Depends(database_city_id_params)]
