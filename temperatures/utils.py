import aiohttp
from fastapi import HTTPException

from settings import settings


async def fetch_temperature_from_api(city_name: str) -> float:
    async with aiohttp.ClientSession() as session:
        url = (
            f"{settings.WEATHER_API_URL}"
            f"?key={settings.WEATHER_API_KEY}"
            f"&q={city_name}"
        )
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data["current"]["temp_c"]
            else:
                raise HTTPException(
                    status_code=response.status,
                    detail="Error occurred while fetching from Weather API"
                )
