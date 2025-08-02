from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_temperature(db: AsyncSession, temp_data: schemas.TemperatureCreate) -> models.Temperature:
    query = insert(models.Temperature).values(**temp_data.dict()).returning(models.Temperature.id)
    result = await db.execute(query)
    new_id = result.scalar_one()
    await db.commit()

    result = await db.execute(select(models.Temperature).where(models.Temperature.id == new_id))
    return result.scalar_one()

async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()

async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.Temperature).where(models.Temperature.city_id == city_id))
    return result.scalars().all()