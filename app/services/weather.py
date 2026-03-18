import httpx

async def fetch_temperature(latitude: float, longitude: float) -> float:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    return data.get("current_weather", {}).get("temperature", 0.0)
