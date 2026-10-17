import httpx


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient(timeout=15.0) as client:
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json",
            },
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        results = geo_data.get("results", [])
        if not results:
            raise ValueError(f"Could not locate city: {city_name}")

        latitude = results[0]["latitude"]
        longitude = results[0]["longitude"]


        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        return float(weather_data["current"]["temperature_2m"])