from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature.models import DBTemperature
from city import models as city_models
from temperature import models as temperature_models
from temperature.utils import fetch_temperature_data


async def get_temperatures(db: AsyncSession, city_id: int = None):
    query = select(DBTemperature).options(
        selectinload(DBTemperature.city)
    )
    if city_id:
        query = query.where(DBTemperature.city_id == city_id)

    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def update_temperatures(db: AsyncSession):
    cities = await db.execute(select(city_models.DBCity))
    for city in cities.scalars():
        temp_c = await fetch_temperature_data(city_name=city.name)
        await db.execute(insert(temperature_models.DBTemperature).values(
            city_id=city.id,
            temperature=temp_c
        ))
    await db.commit()
