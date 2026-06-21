import httpx
from fastapi import HTTPException
from starlette import status


async def fetch_coordinates(client: httpx.AsyncClient, city_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
    response = await client.get(url)

    if response.status_code == 200 and response.json().get("results"):
        data = response.json()["results"][0]
        return data["latitude"], data["longitude"]
    return None, None


async def fetch_weather_by_coords(client: httpx.AsyncClient, lat: float, lon: float) -> float:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to retrieve weather data."
        )

    return response.json()["current_weather"]["temperature"]
