import httpx


CITY_COORDINATES = {
    "Kyiv": {"lat": 50.45, "lon": 30.52},
    "Lviv": {"lat": 49.84, "lon": 24.03},
    "Odesa": {"lat": 46.48, "lon": 30.73},
    "Kharkiv": {"lat": 49.99, "lon": 36.23},
}


async def fetch_temperature(city_name: str) -> float:
    coords = CITY_COORDINATES.get(city_name)
    if not coords:
        raise ValueError(f"No coordinates for city {city_name}")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()

    data = response.json()
    return data["current"]["temperature_2m"]
