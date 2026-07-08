import httpx

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_current_temperature(city_name: str) -> float | None:
    async with httpx.AsyncClient(timeout=10) as client:
        geo_resp = await client.get(
            GEOCODE_URL,
            params={"name": city_name, "count": 1}
        )
        geo_data = geo_resp.json()
        results = geo_data.get("results")
        if not results:
            return None
        lat, lon = results[0]["latitude"], results[0]["longitude"]

        weather_resp = await client.get(
            WEATHER_URL, params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            }
        )
        weather_data = weather_resp.json()
        return weather_data.get("current_weather", {}).get("temperature")
