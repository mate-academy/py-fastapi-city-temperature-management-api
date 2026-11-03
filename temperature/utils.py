import logging

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

logger = logging.getLogger(__name__)


async def get_coordinates(
    client: httpx.AsyncClient, city_name: str
) -> tuple[float, float] | None:
    response = await client.get(
        GEOCODING_URL, params={"name": city_name, "count": 1}
    )
    response.raise_for_status()

    results = response.json().get("results")
    if not results:
        return None

    return results[0]["latitude"], results[0]["longitude"]


async def get_current_temperature(
    client: httpx.AsyncClient, city_name: str
) -> float | None:
    try:
        coordinates = await get_coordinates(client, city_name)
        if coordinates is None:
            logger.warning("City %r was not found by geocoding", city_name)
            return None

        latitude, longitude = coordinates
        response = await client.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )
        response.raise_for_status()

        return float(response.json()["current"]["temperature_2m"])
    except (
        httpx.HTTPError,
        AttributeError,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        logger.warning(
            "Failed to fetch temperature for %r: %r", city_name, error
        )
        return None
