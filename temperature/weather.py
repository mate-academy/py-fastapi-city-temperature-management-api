import httpx

from settings import settings


class CityNotFoundError(Exception):
    """Could not geocode this city name."""


async def geocode_city(
    client: httpx.AsyncClient, city_name: str
) -> tuple[float, float]:
    response = await client.get(
        settings.GEOCODING_URL,
        params={"name": city_name, "count": 1},
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        raise CityNotFoundError(city_name)

    return results[0]["latitude"], results[0]["longitude"]


async def fetch_current_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    latitude, longitude = await geocode_city(client, city_name)

    response = await client.get(
        settings.FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
        },
    )
    response.raise_for_status()
    data = response.json()

    return data["current_weather"]["temperature"]
