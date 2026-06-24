import httpx
from fastapi import HTTPException, status


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        try:
            geo_response = await client.get(geo_url, timeout=10.0)
            geo_response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External geocoding error for city: {city_name}",
            )

        geo_data = geo_response.json()
        if not geo_data.get("results"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City '{city_name}' not found in weather geocoding service",
            )

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        try:
            weather_response = await client.get(weather_url, timeout=10.0)
            weather_response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="External weather service error",
            )

        weather_data = weather_response.json()
        return weather_data["current_weather"]["temperature"]
