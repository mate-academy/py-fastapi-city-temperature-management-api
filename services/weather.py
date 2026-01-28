from __future__ import annotations

import httpx

from core.config import OPEN_METEO_FORECAST_URL, OPEN_METEO_GEOCODING_URL

class WeatherError(Exception):
    pass

async def _geocode_city(client: httpx.AsyncClient, name: str) -> tuple[float, float]:
    r = await client.get(OPEN_METEO_GEOCODING_URL,
                         params={"name": name, "count": 1})
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        raise WeatherError(f"City not found in geocoding: {name}")
    return float(results[0]["latitude"]), float(results[0]["longitude"])

async def fetch_current_temperature_celsius(city_name: str) -> float:
    async with httpx.AsyncClient(timeout=10) as client:
        lat, lon = await _geocode_city(client, city_name)

        r = await client.get(
            OPEN_METEO_FORECAST_URL,
            params={"latitude": lat,
                    "longitude": lon,
                    "current_weather": "true"},
        )
        r.raise_for_status()
        data = r.json()

        cw = data.get("current_weather")
        if not cw or "temperature" not in cw:
            raise WeatherError(f"No current_weather.temperature for {city_name}")
        return float(cw["temperature"])
