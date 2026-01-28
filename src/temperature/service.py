import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.city.crud import get_cities
from src.temperature.crud import create_temperature
from src.temperature.schemas import TemperatureCreate

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def update_temperatures(db: AsyncSession):
    cities = await get_cities(db)

    if not cities:
        return {"message": "No cities found"}

    async with httpx.AsyncClient() as client:
        updated_count = 0

        for city in cities:
            try:
                geo_resp = await client.get(GEOCODING_URL,
                                            params={"name": city.name,
                                                    "count": 1})
                geo_data = geo_resp.json()

                if not geo_data.get("results"):
                    print(f"City not found: {city.name}")
                    continue

                location = geo_data["results"][0]
                lat, lon = location["latitude"], location["longitude"]

                weather_resp = await client.get(WEATHER_URL, params={
                    "latitude": lat,
                    "longitude": lon,
                    "current_weather": "true"
                })
                weather_data = weather_resp.json()
                current_temp = weather_data["current_weather"]["temperature"]

                temp_data = TemperatureCreate(
                    city_id=city.id,
                    temperature=current_temp
                )
                await create_temperature(db, temp_data)
                updated_count += 1

            except Exception as e:
                print(f"Error updating {city.name}: {e}")

    return {
        "message": f"Successfully updated temperatures for {updated_count} cities"}
