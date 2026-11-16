"""Async client for Open-Meteo geocoding and current weather."""

from dataclasses import dataclass
from datetime import datetime, timezone

import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherDataError(Exception):
    """Raised when a city cannot be geocoded or weather data is unavailable."""


@dataclass(frozen=True)
class WeatherReading:
    temperature: float
    date_time: datetime


def _parse_utc_time(value: object) -> datetime:
    if not isinstance(value, str):
        raise WeatherDataError("Weather provider returned an invalid observation time")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise WeatherDataError("Weather provider returned an invalid observation time") from exc
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


async def fetch_current_temperature(
    city_name: str,
    client: httpx.AsyncClient,
) -> WeatherReading:
    """Geocode a city and fetch its current temperature using Open-Meteo."""
    try:
        geocoding_response = await client.get(
            GEOCODING_URL,
            params={"name": city_name, "count": 1, "language": "en", "format": "json"},
        )
        geocoding_response.raise_for_status()
        geocoding_data = geocoding_response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise WeatherDataError(f"City lookup failed: {exc}") from exc

    results = geocoding_data.get("results") if isinstance(geocoding_data, dict) else None
    if not results:
        raise WeatherDataError("No matching city was found by the weather provider")

    location = results[0]
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        raise WeatherDataError("City lookup returned invalid coordinates")

    try:
        weather_response = await client.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
                "timezone": "UTC",
            },
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise WeatherDataError(f"Current weather request failed: {exc}") from exc

    current = weather_data.get("current") if isinstance(weather_data, dict) else None
    if not isinstance(current, dict):
        raise WeatherDataError("Weather provider returned no current conditions")

    temperature = current.get("temperature_2m")
    if not isinstance(temperature, (int, float)):
        raise WeatherDataError("Weather provider returned an invalid temperature")

    return WeatherReading(
        temperature=float(temperature),
        date_time=_parse_utc_time(current.get("time")),
    )

