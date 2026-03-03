import os
import asyncio
import httpx
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature.models import Temperature

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_temperature_by_city_name(city_name: str) -> float | None:
    params = {
        "q": city_name,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                WEATHER_API_URL,
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return data["main"]["temp"]
        except Exception:
            return None


async def update_temperatures_for_all_cities(db: AsyncSession) -> dict:
    """
    Update temperatures for all cities.
    Returns a dictionary with results.
    """
    if not OPENWEATHER_API_KEY:
        return {
            "success": False,
            "error": "API key not found",
            "updated_count": 0
        }

    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        return {
            "success": True,
            "updated_count": 0,
            "message": "No cities found"
        }

    updated_count = 0
    failed_cities = []
    results = []

    for city in cities:
        temperature = await fetch_temperature_by_city_name(city.name)

        if temperature is None:
            failed_cities.append(city.name)
            continue

        db_temperature = Temperature(
            city_id=city.id,
            temperature=temperature,
            date_time=datetime.utcnow()
        )
        db.add(db_temperature)
        updated_count += 1

        results.append({
            "city": city.name,
            "temperature": temperature,
            "success": True
        })

        await asyncio.sleep(1)

    await db.commit()

    return {
        "success": True,
        "updated_count": updated_count,
        "total_cities": len(cities),
        "failed_cities": failed_cities,
        "results": results,
        "message": f"Updated {updated_count} out of {len(cities)} cities"
    }
