import httpx
from fastapi import HTTPException


async def fetch_weather(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_resp = await client.get(geo_url)
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            raise HTTPException(status_code=404, detail=f"Coordinates for {city_name} not found")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = await client.get(weather_url)
        weather_data = weather_resp.json()

        return weather_data["current_weather"]["temperature"]