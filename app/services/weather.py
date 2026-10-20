"""Asynchronous Open-Meteo integration."""

from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherServiceError(RuntimeError):
    """Raised when current weather cannot be retrieved or decoded."""


@dataclass(frozen=True, slots=True)
class CurrentTemperature:
    date_time: datetime
    temperature: float


class WeatherService(Protocol):
    async def fetch_current_temperature(self, city_name: str) -> CurrentTemperature:
        """Fetch the latest temperature for a city."""


class OpenMeteoWeatherService:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def fetch_current_temperature(self, city_name: str) -> CurrentTemperature:
        try:
            geocoding_response = await self.client.get(
                GEOCODING_URL,
                params={"name": city_name, "count": 1, "format": "json"},
            )
            geocoding_response.raise_for_status()
            locations = geocoding_response.json().get("results") or []
            if not locations:
                raise WeatherServiceError(f"city '{city_name}' was not found")

            location = locations[0]
            weather_response = await self.client.get(
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
            observed_at = datetime.fromisoformat(current["time"])
            if observed_at.tzinfo is None:
                observed_at = observed_at.replace(tzinfo=UTC)

            return CurrentTemperature(
                date_time=observed_at,
                temperature=float(current["temperature_2m"]),
            )
        except WeatherServiceError:
            raise
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise WeatherServiceError(
                f"could not fetch weather for '{city_name}'"
            ) from exc


async def get_weather_service() -> AsyncGenerator[WeatherService, None]:
    """Provide a shared async HTTP client for one update request."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield OpenMeteoWeatherService(client)
