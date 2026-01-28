import httpx


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherError(Exception):
    pass


async def fetch_current_temperature(city_name: str) -> float:
    """
    1) Geocode city name -> lat/lon
    2) Fetch current temperature (2m) from Open-Meteo
    """
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        # 1) Geocode
        geo_resp = await client.get(GEOCODE_URL, params={"name": city_name, "count": 1, "language": "en", "format": "json"})
        geo_resp.raise_for_status()
        geo = geo_resp.json()
        results = geo.get("results") or []
        if not results:
            raise WeatherError(f"Geocoding: city '{city_name}' not found")

        lat = results[0]["latitude"]
        lon = results[0]["longitude"]

        # 2) Current weather
        w_resp = await client.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m",
            },
        )
        w_resp.raise_for_status()
        w = w_resp.json()
        current = w.get("current") or {}
        temp = current.get("temperature_2m")
        if temp is None:
            raise WeatherError("Weather: missing temperature_2m in response")

        return float(temp)
