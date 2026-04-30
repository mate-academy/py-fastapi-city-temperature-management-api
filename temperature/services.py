import asyncio
from datetime import datetime

from httpx import AsyncClient, HTTPStatusError
from fastapi import HTTPException

from config import settings
from city.models import City


async def fetch_one_temp(async_client: AsyncClient, city: City) -> dict:
    response = await async_client.get(
        f"{settings.WEATHER_API_URL}/current.json?key={settings.WEATHER_API_KEY}&q={city.name}"
    )
    try:
        response.raise_for_status()
        response = response.json()["current"]
        temp = {
            "date_time": datetime.fromisoformat(response["last_updated"]),
            "temperature": response["temp_c"],
            "city_id": city.id,
        }
        return temp
    except HTTPStatusError:
        raise HTTPException(status_code=response.status_code)
    except KeyError:
        raise HTTPException(status_code=400)


async def fetch_temperature_data(
    async_client: AsyncClient, cities_list: list[City]
) -> list[dict]:
    tasks = [fetch_one_temp(async_client, city) for city in cities_list]
    return await asyncio.gather(*tasks)
