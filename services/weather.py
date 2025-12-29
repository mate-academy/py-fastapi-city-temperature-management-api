import httpx
from fastapi import HTTPException


async def get_coordinates(city_name: str):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        if not data:
            return None, None
        return float(data[0]["lat"]), float(data[0]["lon"])


async def fetch_temperature(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Weather service unavailable")

    data = r.json()

    current = data.get("current_weather")
    if not current:
        raise HTTPException(status_code=502, detail="Invalid weather response")

    temperature = current.get("temperature")
    if temperature is None:
        raise HTTPException(status_code=502, detail="Temperature not found")

    return temperature
