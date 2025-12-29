import os

import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY is not set")



async def fetch_temperature_by_city_name(city_name: str) -> Optional[int]:
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(OPEN_WEATHER_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

            temp = data.get("main", {}).get("temp")
            if temp is None:
                return None

            return int(round(float(temp)))

    except httpx.HTTPError:
        return None
