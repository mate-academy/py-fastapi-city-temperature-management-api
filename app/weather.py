import httpx
from settings import settings


api_key = settings.OPENWEATHER_API_KEY


async def get_temperature_from_api(city_name: str) -> float:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
        temperature = data["main"]["temp"]
        return temperature
