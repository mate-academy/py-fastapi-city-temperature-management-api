import json

import httpx
from fastapi import HTTPException

from settings import settings


WEATHER_URL = (
    f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_TOKEN}"
)


async def get_temperature(city_name: str, city_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL + f"&q={city_name}")

        if response.status_code == 200:
            return {
                "temp": response.json()["current"]["temp_c"],
                "id": city_id
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=(
                    f"City = '{city_name}', "
                    + json.loads(response.content)["error"]["message"]
                ),
            )
