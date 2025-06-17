import httpx
import os
from dotenv import load_dotenv

load_dotenv()


async def get_current_temperature(city_name: str) -> float | None:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = await response.json()
            return data["main"]["temp"]
    return None
