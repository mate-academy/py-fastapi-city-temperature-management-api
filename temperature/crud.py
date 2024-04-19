import asyncio
from datetime import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models as city_models
from city.crud import get_all_cities
from temperature.utils import get_temperature
from temperature import models


async def update_temperature_for_all_cities(db: AsyncSession):
    cities = await get_all_cities(db)
    temperatures = await asyncio.gather(*[get_temperature(city.name) for city in cities])
    temperatures = {temp[0]: temp[1] for temp in temperatures}
    print(temperatures)

    response = []

    for city in cities:
        city_name = city.name
        date_time = datetime.now()
        temperature = temperatures[city_name]

        query = insert(models.DBTemperature).values(
            city_id=city.id,
            date_time=date_time,
            temperature=temperature
        )
        result = await db.execute(query)

        response.append(dict(
            id=result.lastrowid,
            city_id=city.id,
            date_time=date_time,
            temperature=temperature
        ))

    await db.commit()
    return response


async def get_all_temperature_records(db: AsyncSession):
    query = select(models.DBTemperature)
    records = await db.execute(query)
    return [record[0] for record in records.fetchall()]


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = (
        select(models.DBTemperature).
        filter(models.DBTemperature.city_id == city_id)
    )
    records = await db.execute(query)
    return [record[0] for record in records.fetchall()]
