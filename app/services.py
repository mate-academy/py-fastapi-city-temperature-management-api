from dataclasses import dataclass
from datetime import datetime

import httpx


class WeatherServiceError(RuntimeError):
    pass


@dataclass(frozen=True)
class CurrentWeather:
    date_time: datetime
    temperature: float


async def fetch_current_temperature(
    client: httpx.AsyncClient, city_name: str
) -> CurrentWeather:
    """Resolve a city with Open-Meteo and fetch its current temperature."""
    try:
        geocoding = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1, "format": "json"},
        )
        geocoding.raise_for_status()
        results = geocoding.json().get("results") or []
        if not results:
            raise WeatherServiceError(f"City {city_name!r} was not found")

        location = results[0]
        weather = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m",
                "timezone": "UTC",
            },
        )
        weather.raise_for_status()
        current = weather.json()["current"]
        return CurrentWeather(
            date_time=datetime.fromisoformat(current["time"]),
            temperature=float(current["temperature_2m"]),
        )
    except WeatherServiceError:
        raise
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
        raise WeatherServiceError(f"Unable to fetch weather for {city_name!r}") from exc
