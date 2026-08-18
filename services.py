import httpx


async def fetch_city_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:

        geo_url = (f"https://geocoding-api.open-meteo.com/v1/"
                   f"search?name={city_name}&count=1")
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            raise ValueError(f"City {city_name} not "
                             f"found in geocoding service")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = (f"https://api.open-meteo.com/v1/forecast?"
                       f"latitude={lat}&longitude={lon}&current_weather=true")
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()

        return weather_data["current_weather"]["temperature"]
