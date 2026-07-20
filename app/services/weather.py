import httpx
from fastapi import HTTPException

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_current_temperature(latitude: float, longitude: float) -> float:
    """
    Fetches the current temperature for given coordinates using Open-Meteo API.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPEN_METEO_URL, params=params, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch weather data: {str(e)}"
            )

    data = response.json()
    return data["current_weather"]["temperature"]
