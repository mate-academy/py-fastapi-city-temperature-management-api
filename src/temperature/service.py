import asyncio
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.city.crud import get_cities
from src.temperature.crud import create_temperature
from src.temperature.schemas import TemperatureCreate
from src.city.models import DBCity

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_weather_for_city(client: httpx.AsyncClient, city: DBCity):
    try:
        geo_resp = await client.get(GEOCODING_URL,
                                    params={"name": city.name, "count": 1})
        geo_resp.raise_for_status()

        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {
                "status": "error",
                "city": city.name,
                "detail": "City not found in Geocoding API"
            }

        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]

        weather_resp = await client.get(WEATHER_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        })
        weather_resp.raise_for_status()

        weather_data = weather_resp.json()
        current_temp = weather_data["current_weather"]["temperature"]

        return {
            "status": "success",
            "city_id": city.id,
            "city_name": city.name,
            "temperature": current_temp
        }

    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "city": city.name,
            "detail": f"HTTP Error: {e.response.status_code}"
        }
    except Exception as e:
        return {
            "status": "error",
            "city": city.name,
            "detail": str(e)
        }


async def update_temperatures(db: AsyncSession):
    cities = await get_cities(db)

    if not cities:
        return {"message": "No cities found", "errors": []}

    async with httpx.AsyncClient() as client:
        tasks = [fetch_weather_for_city(client, city) for city in cities]

        results = await asyncio.gather(*tasks)

    success_count = 0
    errors = []

    for result in results:
        if result["status"] == "success":
            temp_data = TemperatureCreate(
                city_id=result["city_id"],
                temperature=result["temperature"]
            )
            await create_temperature(db, temp_data)
            success_count += 1
        else:
            errors.append({
                "city": result["city"],
                "detail": result["detail"]
            })

    return {
        "message": "Update complete",
        "total_cities": len(cities),
        "successful_updates": success_count,
        "errors": errors
    }
