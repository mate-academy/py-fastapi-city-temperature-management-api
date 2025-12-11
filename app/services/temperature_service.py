import httpx
from typing import Optional
import os


async def fetch_temperature_for_city(city_name: str) -> Optional[float]:
    api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
    
    if api_key == "demo_key":
        return 20.5
    
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("main", {}).get("temp")
    except (httpx.HTTPError, KeyError, ValueError) as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None

