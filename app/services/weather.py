"""
Async client for fetching current temperature data.

We use Open-Meteo (https://open-meteo.com/) because it is free, requires no
API key, and offers a straightforward geocoding + forecast API — good fit for
an async, testable weather lookup by city name.

Flow for a given city name:
    1. Geocoding API resolves "name" -> (latitude, longitude).
    2. Forecast API returns the current temperature for those coordinates.
"""
import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT = 10.0  # seconds


class WeatherLookupError(Exception):
    """Raised when a city's coordinates or current temperature can't be resolved."""


async def _geocode_city(client: httpx.AsyncClient, city_name: str) -> tuple[float, float]:
    response = await client.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1, "language": "en", "format": "json"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results")
    if not results:
        raise WeatherLookupError(f"Could not geocode city '{city_name}'")
    top = results[0]
    return top["latitude"], top["longitude"]


async def fetch_current_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    """
    Fetch the current temperature (Celsius) for a city by name.

    Raises WeatherLookupError if the city cannot be geocoded or the forecast
    request fails.
    """
    latitude, longitude = await _geocode_city(client, city_name)

    response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    current_weather = data.get("current_weather")
    if not current_weather or "temperature" not in current_weather:
        raise WeatherLookupError(
            f"No current temperature data available for '{city_name}'"
        )
    return float(current_weather["temperature"])
