from typing import Optional

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_current_temperature(
    client: httpx.AsyncClient, city_name: str
) -> Optional[float]:
    geo_response = await client.get(
        GEOCODING_URL, params={"name": city_name, "count": 1}
    )
    geo_response.raise_for_status()
    results = geo_response.json().get("results")
    if not results:
        return None

    latitude = results[0]["latitude"]
    longitude = results[0]["longitude"]

    weather_response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
        },
    )
    weather_response.raise_for_status()
    return weather_response.json()["current_weather"]["temperature"]
