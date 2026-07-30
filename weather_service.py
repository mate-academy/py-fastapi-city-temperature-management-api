import asyncio
import json
import urllib.parse
import urllib.request

from settings import settings

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_city_temperature(city_name: str) -> float:
    def fetch():
        params = urllib.parse.urlencode({
            "q": city_name,
            "appid": settings.API_KEY,
            "units": "metric",
        })

        with urllib.request.urlopen(f"{BASE_URL}?{params}") as response:
            data = json.loads(response.read().decode())

        return data["main"]["temp"]

    return await asyncio.to_thread(fetch)