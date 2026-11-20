import httpx

from settings import settings


async def get_temperature(
    client: httpx.AsyncClient,
    city: str
) -> float | None:
    payload = {"q": city, "key": settings.WEATHER_API_KEY}
    try:
        response = await client.get(settings.URL_WEATHER, params=payload)
    except httpx.RequestError:
        return None
    if response.is_success:
        try:
            temperature = response.json()["current"]["temp_c"]
        except (ValueError, KeyError):
            return None
        else:
            return temperature
