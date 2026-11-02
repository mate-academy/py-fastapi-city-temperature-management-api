import asyncio
from datetime import UTC, datetime

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10.0


class WeatherAPIError(Exception):
    pass


async def fetch_city_temperature(
    client: httpx.AsyncClient, city_name: str
) -> tuple[datetime, float]:
    try:
        geo_response = await client.get(
            GEOCODING_URL, params={"name": city_name, "count": 1}
        )
        geo_response.raise_for_status()
        results = geo_response.json().get("results")
        if not results:
            raise WeatherAPIError(f"City '{city_name}' not found")

        location = results[0]
        weather_response = await client.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m",
                "timezone": "UTC",
            },
        )
        weather_response.raise_for_status()
        current = weather_response.json()["current"]
    except httpx.HTTPError as exc:
        message = f"Weather service request failed: {exc}"
        raise WeatherAPIError(message) from exc
    except (KeyError, ValueError) as exc:
        message = f"Unexpected weather service response: {exc}"
        raise WeatherAPIError(message) from exc

    recorded_at = datetime.fromisoformat(current["time"]).replace(tzinfo=UTC)
    return recorded_at, float(current["temperature_2m"])


async def fetch_temperatures(
    city_names: list[str],
) -> list[tuple[datetime, float] | WeatherAPIError]:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        return await asyncio.gather(
            *(fetch_city_temperature(client, name) for name in city_names),
            return_exceptions=True,
        )
