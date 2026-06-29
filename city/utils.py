import httpx

COUNT = 1


async def get_city(city_name: str) -> tuple[float, float] | None:
    url_city = (
        f"https://geocoding-api.open-meteo.com/v1/"
        f"search?name={city_name}&count={COUNT}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url_city)
        result = response.json()

    if result["results"][0]["name"].lower() != city_name.lower():
        return None
    latitude = result["results"][0]["latitude"]
    longitude = result["results"][0]["longitude"]

    return latitude, longitude


async def get_weather(city_name: str) -> float | None:
    coordinates = await get_city(city_name)
    if coordinates is None:
        return None
    latitude, longitude = coordinates
    temperature_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current=temperature_2m"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(temperature_url)
        result = response.json()

    return result["current"]["temperature_2m"]
