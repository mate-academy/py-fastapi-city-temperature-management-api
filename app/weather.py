from datetime import datetime

import httpx


class WeatherError(Exception):
    pass


async def get_weather_client():
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client


async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> tuple[datetime, float]:
    try:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1},
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            raise WeatherError(f"City not found: {city_name}")
        location = results[0]
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": location["latitude"], "longitude": location["longitude"],
                    "current": "temperature_2m", "timezone": "UTC"},
        )
        response.raise_for_status()
        current = response.json()["current"]
        return datetime.fromisoformat(current["time"]), float(current["temperature_2m"])
    except (httpx.HTTPError, KeyError, TypeError, ValueError, IndexError) as exc:
        raise WeatherError(f"Weather unavailable for {city_name}") from exc
