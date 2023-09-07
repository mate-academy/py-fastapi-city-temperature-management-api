from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import schemas, models


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    query = insert(models.Temperature).values(**temperature.model_dump())
    return await db.execute(query)


async def get_all_temperatures(db: AsyncSession, city_id):
    query = select(models.Temperature).options(selectinload(models.Temperature.city))

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    temperatures = await db.execute(query)

    return [temperature[0] for temperature in temperatures.fetchall()]
