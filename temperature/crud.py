from datetime import datetime
import os

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from temperature.models import DBTemperature


def get_weather_api_key() -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if api_key is None:
        raise EnvironmentError(
            "The WEATHER_API_KEY environment variable has not been configured"
        )
    return api_key


async def fetch_temperature_data(city_name: str, api_key: str) -> dict:
    url = "http://api.weatherapi.com/v1/current.json"
    payload = {"key": api_key, "q": city_name}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=payload)
        response.raise_for_status()
        return response.json()


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None
) -> list[DBTemperature]:
    async with db.begin():
        query = select(DBTemperature)
        if city_id:
            query = query.filter(DBTemperature.city_id == city_id)
        result = await db.execute(query)
        return result.scalars().all()


async def get_latest_temperature_from_external_api(
        city_name: str
) -> tuple[float, datetime]:
    api_key = get_weather_api_key()
    data = await fetch_temperature_data(city_name, api_key)

    temperature = data["current"]["temp_c"]
    date_time = datetime.strptime(
        data["current"]["last_updated"],
        "%Y-%m-%d %H:%M"
    )
    return temperature, date_time


async def update_city_temperature(
        db: AsyncSession,
        db_temperature: DBTemperature
) -> DBTemperature:
    temperature, date_time = await (
        get_latest_temperature_from_external_api(db_temperature.city.name)
    )
    async with db.begin():
        db_temperature.temperature = temperature
        db_temperature.date_time = date_time
        await db.commit()
        await db.refresh(db_temperature)

    return db_temperature
