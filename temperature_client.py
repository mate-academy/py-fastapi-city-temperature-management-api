import httpx


async def fetch_current_temperature(city_name: str) -> float:
    """
    Fetch current temperature for a city.

    Uses Open-Meteo geocoding + forecast API (no key required).
    If the city can't be resolved or response is incomplete, raises ValueError.

    httpx exceptions (network/HTTP errors) may propagate.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1},
        )
        geo.raise_for_status()
        geo_data = geo.json()
        results = geo_data.get("results") or []
        if not results:
            raise ValueError(f"Unknown city: {city_name}")
        lat = results[0].get("latitude")
        lon = results[0].get("longitude")
        if lat is None or lon is None:
            raise ValueError(f"City coordinates missing: {city_name}")

        forecast = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
        )
        forecast.raise_for_status()
        data = forecast.json()
        current = data.get("current_weather") or {}
        temp = current.get("temperature")
        if temp is None:
            raise ValueError(f"No temperature for city: {city_name}")
        return float(temp)

