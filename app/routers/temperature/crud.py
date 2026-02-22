from datetime import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from ..cities.crud import get_cities
from . import models


async def get_temperatures(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Temperature]:
    stmt = select(models.Temperature).options(selectinload(models.Temperature.city)).offset(skip).limit(limit)
    result = await db.execute(stmt)

    return result.scalars().all()




URL_WEATHER = "https://api.open-meteo.com/v1/forecast"

async def update_temperatures(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Temperature]:

    def url_geo_locate(name: str):
        return f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language=en&format=json"

    cities = await get_cities(db=db)

    async with httpx.AsyncClient() as client:
        for city in cities:

            url = url_geo_locate(str(city.name))
            try:
                geo_data = await client.get(url)
                geo_data.raise_for_status()
                geo_data = geo_data.json()

                params = {
                    "latitude": geo_data["results"][0]["latitude"],
                    "longitude": geo_data["results"][0]["longitude"],
                    "hourly": "temperature_2m"
                }

                weather_response = await client.get(URL_WEATHER, params=params)

                weather_response.raise_for_status()

                temperatures = weather_response.json()

                format_string = "%Y-%m-%dT%H:%M"

                for time, temp in zip(temperatures["hourly"]["time"], temperatures["hourly"]["temperature_2m"]):
                    new_temp = models.Temperature(city_id=city.id,
                                                  date_time=datetime.strptime(time, format_string),
                                                  temperature=temp)

                    db.add(new_temp)
            except IndexError, KeyError, httpx.HTTPStatusError:
                pass


        await db.commit()

    return await get_temperatures(db=db, skip=skip, limit=limit)



async def delete_temperatures(db: AsyncSession):
    await db.execute(delete(models.Temperature))
    await db.commit()


async def temperature_by_id(db: AsyncSession, city_id: int, skip: int = 0, limit: int = 100) -> list[models.Temperature]:
    temperatures = await db.scalars(
        select(models.Temperature
               ).where(
            models.Temperature.city_id==city_id
        ).offset(skip).limit(limit))

    return temperatures.all()
