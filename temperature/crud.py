import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from . import models, schemas, utils
from .schemas import TemperatureCreate


async def get_temperatures(db: AsyncSession, id: int):
    query = select(models.Temperature)
    if id != -1:
        query = query.where(models.Temperature.city_id == id)
    temperatures_list = await db.execute(query)

    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
):
    query = insert(models.Temperature).values(**temperature.model_dump())

    return await db.execute(query)


async def update_city_temperature(city: City, db: AsyncSession):
    temperature = await utils.get_temperature(city.name)
    temperature_data = TemperatureCreate(
        city_id=city.id,
        temperature=temperature,
        date_time=datetime.datetime.now()
    )
    await create_temperature(db=db, temperature=temperature_data)
