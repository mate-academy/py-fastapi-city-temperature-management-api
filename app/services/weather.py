import httpx
from fastapi import HTTPException


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def get_city_coordinates(
    client: httpx.AsyncClient,
    city_name: str,
) -> tuple[float, float]:

    try:
        response = await client.get(
            GEOCODING_URL,
            params={
                "name": city_name,
                "count": 1,
            },
        )
        response.raise_for_status()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to find coordinates for {city_name}",
        ) from exc

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"City {city_name} not found",
        )

    city = results[0]

    return city["latitude"], city["longitude"]


async def get_current_temperature(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
) -> float:

    try:
        response = await client.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )
        response.raise_for_status()

        data = response.json()
        return float(data["current"]["temperature_2m"])

    except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch temperature",
        ) from exc
