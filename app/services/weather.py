import httpx


async def fetch_temperature(lat: float, lon: float) -> float:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    return data["current_weather"]["temperature"]
