import httpx

from settings import settings


async def get_coords(
        client: httpx.AsyncClient, city_name: str
) -> tuple[float, float] | None:
    r = await client.get(
        settings.GEOCODING_API_URL,
        params={
            "name": city_name,
            "count": 1,
            "language": "ru",
            "format": "json"
        },
    )
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        return None
    return results[0]["latitude"], results[0]["longitude"]


async def get_current_temp(
        client: httpx.AsyncClient,
        lat: float,
        lon: float
) -> tuple[str, float]:
    r = await client.get(
        settings.WEATHER_API_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "timezone": "UTC"
        },
    )
    r.raise_for_status()
    data = r.json()
    cur = data["current"]
    return cur["time"], cur["temperature_2m"]
