from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models
from temperature.temp_API import get_temperature
import datetime


async def create_new_temp_record(
        session: AsyncSession,
        city_name: str,
        country: str):
    temperature = await get_temperature(country, city_name)
    date_time = datetime.datetime.now(datetime.UTC)
    query = (insert(models.DBTemperature).
             values(city_name=city_name,
                    date_time_utc=date_time,
                    temperature=temperature))

    await session.execute(query)
    await session.commit()

    return (f"{date_time.strftime("%d/%m/%Y %H:%M:%S")}UTC - "
            f"current temperature value in {city_name} was added to the database")


async def get_all_records(session: AsyncSession,
                          skip: int = 0,
                          limit: int = 10):
    query = (select(models.DBTemperature).
             offset(skip).limit(limit))
    temp_data = await session.execute(query)
    return [record[0] for record in temp_data.all()]


async def get_city_records(session: AsyncSession,
                           city_name: str,
                           skip: int = 0,
                           limit: int = 10):
    query = (select(models.DBTemperature).
             where(models.DBTemperature.city_name == city_name).
             offset(skip).limit(limit))
    temp_data = await session.execute(query)
    return [record[0] for record in temp_data.all()]
