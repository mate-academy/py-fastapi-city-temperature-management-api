import httpx

from config import settings

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


class WeatherFetchError(Exception):
    pass


async def fetch_current_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    params = {"key": settings.WEATHERAPI_KEY, "q": city_name}

    try:
        response = await client.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise WeatherFetchError(
            f"WeatherAPI returned {exc.response.status_code} for '{city_name}'"
        ) from exc
    except httpx.RequestError as exc:
        raise WeatherFetchError(f"Network error fetching '{city_name}': {exc}") from exc

    data = response.json()
    try:
        return float(data["current"]["temp_c"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherFetchError(
            f"Unexpected response shape for '{city_name}': {data}"
        ) from exc
