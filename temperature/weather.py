import httpx


async def get_temperature(latitude: float, longitude: float) -> float:
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    data = response.json()

    return data["current"]["temperature_2m"]


async def get_coordinates(city_name: str) -> tuple[float, float]:
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    data = response.json()

    city = data["results"][0]

    return city["latitude"], city["longitude"]
