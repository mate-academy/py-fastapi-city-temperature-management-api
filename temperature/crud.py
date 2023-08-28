from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import models, schemas


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
):
    query = insert(models.Temperature).values(**temperature.model_dump())
    return await db.execute(query)


async def get_temperatures(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        city_id: int = None

):
    query = select(
        models.Temperature
    ).options(
        selectinload(models.Temperature.city)
    ).offset(
        skip
    ).limit(
        limit
    )
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]
