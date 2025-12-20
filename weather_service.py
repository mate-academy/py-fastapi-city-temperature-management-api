import httpx


async def get_current_temp(city_name: str) -> float:
    # 1. Get Lat/Lon for the city name (Geocoding)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    async with httpx.AsyncClient() as client:
        geo_resp = await client.get(geo_url)
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            return 0.0  # Or raise an error

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # 2. Get Weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = await client.get(weather_url)
        return weather_resp.json()["current_weather"]["temperature"]