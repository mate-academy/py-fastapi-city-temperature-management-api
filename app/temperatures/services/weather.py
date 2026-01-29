import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_current_temperature(lat: float, lon: float) -> float:
    timeout = httpx.Timeout(5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            OPEN_METEO_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
            },
        )
        response.raise_for_status()
        data = response.json()

    return data["current_weather"]["temperature"]
