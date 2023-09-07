from datetime import datetime

from sqlalchemy import distinct
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models
from temperature import schemas
from city import models
from temperature.temperatures_manager import get_temperature


async def update_temperatures(data_base):
    cities = await data_base.execute(select(models.DBCity))

    for city in cities.scalars():
        city_temp = await get_temperature(city.name)
        date_time = datetime.utcnow()

        data_base.add(
            models.DBTemperature(city_id=city.id, date_time=date_time, temperature=city_temp)
        )


    await data_base.commit()


async def get_all_temperatures(data_base, skip: int, limit: int) -> list:
    queryset = select(models.DBTemperature).offset(skip).limit(limit)
    temperatures = await data_base.execute(queryset)
    return [temp[0] for temp in temperatures.fetchall()]

