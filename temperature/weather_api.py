import httpx

from settings import settings


async def get_temperature(
    client: httpx.AsyncClient,
    city: str
) -> float | None:
    payload = {"q": city, "key": settings.WEATHER_API_KEY}
    try:
        response = await client.get(settings.URL_WEATHER, params=payload)
    except httpx.TimeoutException:
        return None
    if response.is_success:
        return response.json()["current"]["temp_c"]
