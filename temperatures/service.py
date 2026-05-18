import httpx

async def fetch_temperature(city_name: str) -> float | None:
    async with httpx.AsyncClient() as client:
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1},
        )
        geo_data = geo_response.json()
        results = geo_data.get("results")
        if not results:
            return None
        lat = results[0]["latitude"]
        lon = results[0]["longitude"]

        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
        )
        weather_data = weather_response.json()
        temperature = weather_data["current_weather"]["temperature"]
        return temperature
