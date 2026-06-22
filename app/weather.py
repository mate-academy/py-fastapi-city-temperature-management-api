import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherLookupError(Exception):
    """Raised when the current temperature for a city cannot be retrieved."""


async def fetch_current_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    """Look up a city's coordinates and return its current temperature in Celsius."""
    geo_response = await client.get(
        GEOCODING_URL, params={"name": city_name, "count": 1}
    )
    geo_response.raise_for_status()
    geo_results = geo_response.json().get("results")
    if not geo_results:
        raise WeatherLookupError(f"Could not find coordinates for city '{city_name}'")

    latitude = geo_results[0]["latitude"]
    longitude = geo_results[0]["longitude"]

    forecast_response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
        },
    )
    forecast_response.raise_for_status()
    current_weather = forecast_response.json().get("current_weather")
    if not current_weather:
        raise WeatherLookupError(f"No current weather data for city '{city_name}'")

    return current_weather["temperature"]
