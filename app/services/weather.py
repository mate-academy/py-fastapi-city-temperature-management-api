import httpx


async def get_city_coordinates(city_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={
                    "name": city_name,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise RuntimeError("Geocoding service is unavailable") from error

    data = response.json()
    if not data.get("results"):
        raise ValueError(f"City '{city_name}' not found")

    return data["results"][0]


async def get_current_temperature(latitude: float, longitude: float) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m",
                },
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise RuntimeError("Weather service is unavailable") from error

    data = response.json()
    return data["current"]["temperature_2m"]


async def get_temperature_for_city(city_name: str) -> float:
    coordinates = await get_city_coordinates(city_name)

    temperature = await get_current_temperature(
        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],
    )

    return temperature
