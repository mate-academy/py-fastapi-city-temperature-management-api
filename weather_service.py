import httpx
import logging


async def get_current_temp(city_name: str) -> float | None:
    async with httpx.AsyncClient() as client:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
            geo_resp = await client.get(geo_url)
            geo_data = geo_resp.json()

            results = geo_data.get("results")
            if not results:
                return None

            lat = results[0].get("latitude")
            lon = results[0].get("longitude")

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_resp = await client.get(weather_url)
            weather_data = weather_resp.json()

            current_weather = weather_data.get("current_weather")
            if current_weather:
                return current_weather.get("temperature")

            return None
        except (httpx.HTTPError, KeyError, IndexError) as e:
            logging.error(f"Error fetching weather for {city_name}: {e}")
            return None