import httpx

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> float | None:
    geo = await client.get(GEO_URL, params={"name": city_name, "count": 1})
    geo.raise_for_status()
    results = geo.json().get("results")

    if not results:
        return None

    weather = await client.get(
        FORECAST_URL,
        params={
            "lat": results[0].get("latitude"),
            "lon": results[0].get("longitude"),
            "current": "temperature_2m",
        }
    )
    weather.raise_for_status()
    return weather.json()["current"]["temperature_2m"]
