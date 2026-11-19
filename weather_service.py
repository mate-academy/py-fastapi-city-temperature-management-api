import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_city_temperature(city_name: str) -> float | None:
    try:
        async with httpx.AsyncClient() as client:
            geo_response = await client.get(
                GEOCODING_URL,
                params={
                    "name": city_name,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            results = geo_data.get("results")
            if not results:
                return None

            latitude = results[0]["latitude"]
            longitude = results[0]["longitude"]

            weather_response = await client.get(
                WEATHER_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True,
                },
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            return weather_data.get("current_weather", {}).get("temperature")
    except httpx.HTTPError:
        return None
