import httpx


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


async def get_coordinates_by_city_name(city_name: str) -> tuple[float, float]:
    params = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "city-temperature-api"}

    async with httpx.AsyncClient(headers=headers, timeout=10) as client:
        response = await client.get(NOMINATIM_URL, params=params)
        response.raise_for_status()
        data = response.json()

    if not data:
        raise ValueError(f"City '{city_name}' not found")

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])

    return latitude, longitude
