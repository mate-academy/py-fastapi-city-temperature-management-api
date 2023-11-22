import json
from httpx import AsyncClient

from settings import settings

URL = "https://api.weatherapi.com/v1/current.json"


async def create_temperature(city_name: str):
    params = {
        "q": city_name,
        "key": settings.WEATHER_API_KEY
    }

    async with AsyncClient() as client:
        result = await client.get(URL, params=params)
        city_temp = json.loads(result.content)["current"]["temp_c"]

    return city_temp
