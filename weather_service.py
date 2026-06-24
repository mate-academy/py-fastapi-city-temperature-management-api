from datetime import datetime, timezone

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherFetchError(Exception):
    pass


async def fetch_current_temperature(
    client: httpx.AsyncClient, city_name: str
) -> tuple[float, datetime]:
    try:
        geo_response = await client.get(
            GEOCODING_URL, params={"name": city_name, "count": 1}
        )
        geo_response.raise_for_status()
    except httpx.HTTPError as exc:
        raise WeatherFetchError(
            f"Can`t make response for '{city_name}': {exc}"
        ) from exc

    geo_data = geo_response.json()
    results = geo_data.get("results")
    if not results:
        raise WeatherFetchError(f"City '{city_name}' did`t find")

    latitude = results[0]["latitude"]
    longitude = results[0]["longitude"]

    try:
        forecast_response = await client.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
            },
        )
        forecast_response.raise_for_status()
    except httpx.HTTPError as exc:
        raise WeatherFetchError(
            f"Could`t make request for '{city_name}': {exc}"
        ) from exc

    forecast_data = forecast_response.json()
    current = forecast_data.get("current_weather")
    if not current:
        raise WeatherFetchError(f"API did`t return the weather for '{city_name}'")

    temperature = current["temperature"]
    return temperature, datetime.now(timezone.utc)
