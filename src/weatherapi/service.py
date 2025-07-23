from _datetime import datetime

import httpx

from src.config import settings
from src.weatherapi.schemas.temperature import TemperatureBase


async def fetch_weather_from_api(city_name: str) -> TemperatureBase:
    params = {
        "q": city_name,
        "key": settings.WEATHER_API
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(settings.BASE_URL + "/current.json", params=params)
        response.raise_for_status()
        data = response.json()
        return TemperatureBase(
            temperature=data["current"]["temp_c"],
            date_time=datetime.strptime(data["current"]["last_updated"], "%Y-%m-%d %H:%M")
        )
