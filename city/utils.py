import os

import httpx
from dotenv import load_dotenv

from city import schemas

load_dotenv()

WEATHER_URL = os.getenv("WEATHER_BASE_URL")
API_KEY = os.getenv("API_WEATHER_KEY")


async def get_temperature_by_api(
        city_name: str,
        city_id: int,
        client: httpx.AsyncClient,
        weather_url: str = WEATHER_URL,
        api_key: str = API_KEY,

):
    response = await client.get(f"{weather_url}current.json?q={city_name}&key={api_key}")

    if response.status_code == 200:
        data = response.json()
        api_temperature = schemas.TemperatureCreate(
            date_time=data["current"]["last_updated"],
            city_id=city_id,
            temperature=data["current"]["temp_c"]
        )
        return api_temperature

    return [city_name, city_id, response.status_code]
