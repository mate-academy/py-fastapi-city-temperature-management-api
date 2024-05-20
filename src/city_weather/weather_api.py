import httpx

from src.settings import settings


async def get_tepmerature(city: str, client=httpx.AsyncClient()) -> float:
    params = {"key": settings.API_KEY, "q": city}
    response = await client.get(settings.WEATHER_URL, params=params)
    temperature = None
    if response.status_code == 200:
        data = response.json()
        temperature = data["current"]["temp_c"]
    return temperature
