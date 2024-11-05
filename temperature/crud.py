from datetime import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models


async def fetch_current_temperature(city_name: str) -> float:
    """
    Fetches current temperature for a given city from MetaWeather API.
    """
    # Запрос для получения WOEID города
    location_url = f"https://www.metaweather.com/api/location/search/?query={city_name}"
    async with httpx.AsyncClient() as client:
        location_response = await client.get(location_url)
        if location_response.status_code != 200 or not location_response.json():
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found.")

        location_data = location_response.json()
        woeid = location_data[0]["woeid"]

        # Запрос для получения погоды по WOEID
        weather_url = f"https://www.metaweather.com/api/location/{woeid}/"
        weather_response = await client.get(weather_url)
        if weather_response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Weather data for '{city_name}' not found.")

        weather_data = weather_response.json()
        current_weather = weather_data["consolidated_weather"][0]
        temperature = current_weather["the_temp"]

    return temperature


async def get_temperatures(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Temperature).offset(skip).limit(limit))
    return result.scalars().all()


async def fetch_and_store_temperatures(db: AsyncSession, temperatures_data: list):
    for temp in temperatures_data:
        temperature_record = models.Temperature(
            city_id=temp["city_id"],
            date_time=temp["date_time"],
            temperature=temp["temperature"]
        )
        db.add(temperature_record)
    await db.commit()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.Temperature).where(models.Temperature.city_id == city_id))
    return result.scalars().all()