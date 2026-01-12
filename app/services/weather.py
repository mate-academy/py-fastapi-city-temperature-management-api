import httpx


async def get_coordinates(city_name: str) -> tuple[float, float]:
    url = "https://geocoding-api.open-meteo.com/v1/search" f"?name={city_name}&count=1"

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()

    if not data.get("results"):
        raise ValueError(f"City '{city_name}' not found")

    city = data["results"][0]
    return city["latitude"], city["longitude"]


async def get_temperature_by_city_name(city_name: str) -> float:
    lat, lon = await get_coordinates(city_name)

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()

    return data["current_weather"]["temperature"]
