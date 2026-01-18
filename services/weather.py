import httpx
from typing import Optional

async def get_city_coordinates(city_name: str) -> Optional[tuple[float, float]]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return result["latitude"], result["longitude"]
    return None

async def get_current_temperature(lat: float, lon: float) -> Optional[float]:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if "current_weather" in data:
                return data["current_weather"]["temperature"]
    return None

async def fetch_weather_for_city(city_name: str) -> Optional[float]:
    coords = await get_city_coordinates(city_name)
    if coords:
        lat, lon = coords
        return await get_current_temperature(lat, lon)
    return None
