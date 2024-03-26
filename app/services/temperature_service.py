import httpx
from core.config import settings


async def fetch_temperature(city_name: str):
    url = f"http://api.weatherapi.com/v1/current.json?key=\
        {settings.weather_api_key}&q={city_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['current']['temp_c']
    return None
