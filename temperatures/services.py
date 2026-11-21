import httpx

from cities.models import City
from settings import settings
from temperatures.schemas import TemperatureCreate

WEATHER_API_URL = (
    f"https://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}"
)


async def fetch_data(client: httpx.AsyncClient, city: City) -> TemperatureCreate:
    return TemperatureCreate.model_validate(
        {
            "city_id": city.id,
            "temperature": (
                await client.get(WEATHER_API_URL + f"&q={city.name}")
            ).json()["current"]["temp_c"],
        }
    )
