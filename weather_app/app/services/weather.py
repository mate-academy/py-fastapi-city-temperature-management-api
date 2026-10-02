from datetime import datetime, timezone

import httpx

from weather_app.app.config import get_settings


class WeatherFetchError(Exception):
    pass


async def fetch_current_temperature(client: httpx.AsyncClient, city_name: str) -> tuple[float, datetime]:
    settings = get_settings()

    geo_resp = await client.get(settings.geocoding_api_url, params={"name": city_name, "count": 1})
    geo_resp.raise_for_status()
    results = geo_resp.json().get("results")
    if not results:
        raise WeatherFetchError(f"Could not geocode city '{city_name}'")

    latitude, longitude = results[0]["latitude"], results[0]["longitude"]

    forecast_resp = await client.get(
        settings.forecast_api_url,
        params={"latitude": latitude, "longitude": longitude, "current_weather": True},
    )
    forecast_resp.raise_for_status()
    current = forecast_resp.json().get("current_weather")
    if not current or "temperature" not in current:
        raise WeatherFetchError(f"No current weather data for '{city_name}'")

    return float(current["temperature"]), datetime.now(timezone.utc).replace(tzinfo=None)
