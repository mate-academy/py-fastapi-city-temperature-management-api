import httpx


async def geocode_city(city_name: str) -> tuple[float, float] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    results = data.get("results")
    if not results:
        return None

    first = results[0]
    return first["latitude"], first["longitude"]


async def fetch_current_temperature(latitude: float, longitude: float) -> float:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    return data["current_weather"]["temperature"]
