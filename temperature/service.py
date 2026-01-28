import httpx
from fastapi import HTTPException

from core.config import WEATHER_API_KEY, WEATHER_API_URL


async def fetch_temperature(city: str) -> float:
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)

    if response.status_code == 400:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid city name: '{city}'"
        )

    response.raise_for_status()

    data = response.json()
    return data["current"]["temp_c"]