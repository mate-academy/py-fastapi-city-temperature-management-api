import httpx
from httpx import HTTPStatusError

from city_app.schemas import TemperatureDtoCreate
from settings import settings
from .models import City

WEATHER_URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather(city: City, client: httpx.AsyncClient) -> TemperatureDtoCreate:
    try:
        params = {"key": settings.WEATHER_API_KEY, "q": city.name, "aqi": "no"}
        temperature = await client.get(WEATHER_URL, params=params)
        temperature.raise_for_status()
        return TemperatureDtoCreate(temperature=temperature.json()["current"]["temp_c"], city_id=city.id)
    except httpx.HTTPStatusError as e:
        raise Exception(f"Bad request with city {city.name}", e)