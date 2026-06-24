import httpx
from app.config import settings


async def fetch_current_temperature(city_name: str) -> float | None:
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"

    async with httpx.AsyncClient() as client:
        try:
            geo_res = await client.get(geocoding_url)
            geo_data = geo_res.json()

            if not geo_data.get("results"):
                return None

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            }
            weather_res = await client.get(settings.WEATHER_API_URL, params=weather_params)
            weather_data = weather_res.json()

            return weather_data["current_weather"]["temperature"]
        except Exception:
            return None
