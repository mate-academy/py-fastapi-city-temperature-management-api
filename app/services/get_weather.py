import httpx


async def get_weather(lat: float, lon: float) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
            },
        )

    data = response.json()
    try:
        return data["current_weather"]["temperature"]
    except (KeyError, TypeError):
        raise ValueError("Invalid weather API response")
