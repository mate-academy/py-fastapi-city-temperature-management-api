from httpx import AsyncClient

from settings import settings

API_URL = "http://api.weatherapi.com/v1/current.json"


async def get_temperature_for_city(city_name: str, client: AsyncClient):
    response = await client.get(
        API_URL,
        params={"key": settings.WEATHER_API, "q": city_name}
    )

    print(response.status_code)
    if response.status_code == 200:
        return response.json()["current"]["temp_c"]

    return None
