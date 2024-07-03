import datetime
import os
import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv

from temperature import models
from city import crud

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


async def get_all_temperatures(db: AsyncSession) -> [models.Temperature]:
    query = select(models.Temperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_single_city_temperatures(
        db: AsyncSession,
        city_id: int
) -> [models.Temperature]:
    query = (select(models.Temperature)
             .where(models.Temperature.city_id == city_id))
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def update_temperature_data(db: AsyncSession) -> [models.Temperature]:
    cities = await crud.get_all_cities(db)
    temperatures = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(f"{URL}?q={city.name}&key={API_KEY}")
            json_response = response.json()
            if json_response["location"]["name"] != city.name:
                continue
            temperature = models.Temperature(
                date_time=datetime.datetime.strptime(
                    json_response["location"]["localtime"],
                    "%Y-%m-%d %H:%M"
                ),
                temperature=json_response["current"]["temp_c"],
                city_id=city.id
            )
            temperatures.append(temperature)
    db.add_all(temperatures)
    await db.commit()
    return temperatures
