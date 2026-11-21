import httpx
from fastapi import HTTPException

from cities.models import City
from settings import settings
from temperatures.schemas import TemperatureCreate

WEATHER_API_URL = (
    f"https://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}"
)


async def fetch_data(client: httpx.AsyncClient, city: City) -> TemperatureCreate:
    try:
        data = await client.get(WEATHER_API_URL + f"&q={city.name}")
        if "error" in data:
            error_msg = data["error"].get("message", "Unknown provider error")
            raise HTTPException(
                status_code=400, detail=f"WeatherAPI error: {error_msg}"
            )

        return TemperatureCreate.model_validate(
            {"city_id": city.id, "temperature": (data.json()["current"]["temp_c"],)}
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502, detail=f"Network error while fetching weather: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Weather provider error: {e.response.status_code}",
        )
