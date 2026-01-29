import httpx
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(lat: float, lon: float):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(API_URL, params=params, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            temp = data.get("current_weather", {}).get("temperature")
            if temp is None:
                raise ValueError("Temperature data missing in API response")
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as e:
            print(f"Weather API error: {e}")
            return None, None

    return temp, datetime.utcnow()
