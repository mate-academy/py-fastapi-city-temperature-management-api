import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherServiceError(Exception):
    pass


async def get_city_coordinates(
    client: httpx.AsyncClient,
    city_name: str,
) -> tuple[float, float]:
    response = await client.get(
        GEOCODING_URL,
        params={
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    response.raise_for_status()

    data = response.json()
    results = data.get("results")

    if not results:
        raise WeatherServiceError(
            f"City '{city_name}' was not found"
        )

    location = results[0]

    return (
        location["latitude"],
        location["longitude"],
    )


async def get_current_temperature(
    client: httpx.AsyncClient,
    city_name: str,
) -> float:
    latitude, longitude = await get_city_coordinates(
        client=client,
        city_name=city_name,
    )

    response = await client.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
        },
    )

    response.raise_for_status()

    data = response.json()

    return float(
        data["current"]["temperature_2m"]
    )
