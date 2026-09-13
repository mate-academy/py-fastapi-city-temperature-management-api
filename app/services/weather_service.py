import httpx


async def get_coordinates_by_city_name(
        city_name: str
) -> tuple[float, float] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    if data["results"]:
        return (
            data["results"][0]["latitude"],
            data["results"][0]["longitude"]
        )

    return None


async def get_current_temperature(latitude: float, longitude: float) -> float:
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    return data["current"]["temperature_2m"]


async def get_temperature_by_city_name(city_name: str) -> float | None:
    coordinates = await get_coordinates_by_city_name(city_name)

    if coordinates is None:
        return None

    latitude, longitude = coordinates

    return await get_current_temperature(latitude, longitude)
