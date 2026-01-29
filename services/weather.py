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
        resp = await client.get(API_URL, params=params)
        data = resp.json()

    return data["current_weather"]["temperature"], datetime.utcnow()
