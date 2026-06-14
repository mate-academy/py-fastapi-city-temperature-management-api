import httpx


async def get_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:

        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1}
        )

        geo_data = geo.json()

        if "results" not in geo_data:
            return 0

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m"
            }
        )

        return weather.json()["current"]["temperature_2m"]
