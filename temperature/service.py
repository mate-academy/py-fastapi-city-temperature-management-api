import httpx


async def get_current_temp_by_name(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            raise ValueError(f"City '{city_name}' not found")

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
        weather_response = await client.get(weather_url, params=params)
        weather_data = weather_response.json()

        return weather_data["current_weather"]["temperature"]
