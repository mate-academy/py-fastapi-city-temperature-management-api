import httpx
from fastapi import HTTPException
from settings import settings

WEATHER_URL = (
    f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_TOKEN}"
)

async def get_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{WEATHER_URL}&q={city_name}")

        if response.status_code == 200:
            return response.json()["current"]["temp_c"]

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to get temperature for city '{city_name}': {error_message}"
        )
