from httpx import AsyncClient

from cities import models
from settings import settings


async def fetch_temperature_for_city(
    city: models.City, client: AsyncClient
) -> dict | None:
    url = settings.WEATHER_BASE_URL + "current.json"
    resp = await client.get(
        url, params={"key": settings.WEATHER_API_KEY, "q": city.name}
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    temperature = data["current"]["temp_c"]
    return {"city_id": city.id, "temperature": temperature}
