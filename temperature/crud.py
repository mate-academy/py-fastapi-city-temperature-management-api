from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from . import schemas

async def create_temperature(db: AsyncSession, temp_data: schemas.TemperatureCreate):
    query = insert(models.Temperature).values(**temp_data.dict())
    await db.execute(query)
    await db.commit()

async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()

async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.Temperature).where(models.Temperature.city_id == city_id))
    return result.scalars().all()