import httpx
from datetime import datetime


async def fetch_current_temp(
        client: httpx.AsyncClient,
        city_name: str
) -> tuple[float, datetime]:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = await client.get(geo_url,
                                params={"name": city_name, "count": 1})
    geo_data = geo_resp.json()

    if not geo_data.get("results"):
        raise ValueError(f"City '{city_name}' not found")

    location = geo_data["results"][0]
    lat, lon = location["latitude"], location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = await client.get(weather_url, params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    weather_data = weather_resp.json()

    current = weather_data["current_weather"]
    return float(current["temperature"]), datetime.fromisoformat(
        current["time"])
