import httpx

from settings import settings

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_city_temperature(city_name: str) -> float:

    params = {
        "q": city_name,
        "appid": settings.API_KEY,
        "units": "metric",
    }

    async with httpx.AsyncClient(trust_env=False) as client:
        response = await client.get(BASE_URL, params=params)

    response.raise_for_status()

    data = response.json()

    return data["main"]["temp"]
    