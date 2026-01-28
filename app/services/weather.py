import httpx


WEATHER_API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}&current_weather=true"
)


async def get_current_temperature(latitude: float, longitude: float) -> float:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(WEATHER_API_URL.format(lat=latitude, lon=longitude))
        response.raise_for_status()
        data = response.json()

    return data["current_weather"]["temperature"]
