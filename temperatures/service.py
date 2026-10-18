import httpx


async def fetch_temperature_for_city(city_name: str) -> float |None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city_name,
            "count": 1,
            "lang": "en",
            "format": "json",
        }
        geo_response = await client.get(geo_url, params=geo_params)
        if geo_response.status_code != 200:
            return None

        geo_data = geo_response.json()
        results = geo_data.get("results")
        if not results:
            return None

        latitude = results[0]["latitude"]
        longitude = results[0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m"
        }
        weather_response = await client.get(weather_url, params=weather_params)
        if weather_response.status_code != 200:
            return None
        weather_data = weather_response.json()
        current = weather_data.get("current")
        if not current or "temperature_2m" not in current:
            return None

        return float(current["temperature_2m"])