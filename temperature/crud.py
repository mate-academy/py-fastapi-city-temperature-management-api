import asyncio
import os

import httpx
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from dependencies import get_db
from temperature.models import DBTemperature
from temperature.schemas import TemperatureRecord

load_dotenv()

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPENWEATHER_KEY")


async def get_single_city_temperature(
        city_name: str,
        city_id: int,
        client: httpx.AsyncClient
) -> tuple[float | None, int, str] | None:
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    response = await client.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["main"]["temp"], city_id, city_name

    return None, city_id, city_name


async def get_temperatures_in_cities(db: AsyncSession = Depends(get_db)) -> dict:
    query = select(models.DBCity)
    result = await db.execute(query)
    cities_list = [city[0] for city in result.fetchall()]

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[get_single_city_temperature(
                city_name=city.name,
                city_id=city.id,
                client=client
            ) for city in cities_list]
        )

    for single_result in results:
        temperature, city_id, city_name = single_result

        if temperature is not None:
            temp_query = insert(DBTemperature).values(
                city_id=city_id,
                temperature=temperature
            )
            await db.execute(temp_query)
            await db.commit()
        else:
            print(f"Please, check the name of the city: "
                  f"{city_name} is not in the list of possible results!")

    return {"message": "Done!"}


async def get_temperature_records(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None
) -> list[TemperatureRecord]:
    if city_id is not None:
        query = (select(DBTemperature.city_id, func.max(DBTemperature.temperature))
                 .where(DBTemperature.city_id == city_id))
    else:
        query = (
            select(DBTemperature.city_id, func.max(DBTemperature.temperature))
            .group_by(DBTemperature.city_id)
        )

    results = await db.execute(query)

    max_temperatures = []
    for result in results.fetchall():
        query = select(models.DBCity).where(models.DBCity.id == result[0])
        city = await db.execute(query)
        record = TemperatureRecord(
            city_name=city.scalar().name,
            temperature=result[1]
        )
        max_temperatures.append(record)

    return max_temperatures
