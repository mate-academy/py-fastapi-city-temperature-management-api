import httpx


class WeatherServiceError(Exception):
    """Raised when weather data cannot be fetched for a city."""


async def fetch_current_temperature_by_city_name(city_name: str) -> float:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            geo_response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city_name, "count": 1},
            )
            geo_response.raise_for_status()
        except httpx.HTTPError as exc:
            raise WeatherServiceError(
                f"Failed to geocode city '{city_name}': {exc}"
            ) from exc

        results = geo_response.json().get("results")
        if not results:
            raise WeatherServiceError(f"City '{city_name}' not found")

        latitude = results[0]["latitude"]
        longitude = results[0]["longitude"]

        try:
            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True,
                },
            )
            weather_response.raise_for_status()
        except httpx.HTTPError as exc:
            raise WeatherServiceError(
                f"Failed to fetch weather for '{city_name}': {exc}"
            ) from exc

        return weather_response.json()["current_weather"]["temperature"]
