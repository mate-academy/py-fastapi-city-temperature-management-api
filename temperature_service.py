import httpx
import os
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from dotenv import load_dotenv

load_dotenv()

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
# Free tier: current weather data
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_temperature_for_city(city_name: str) -> float | None:
    """
    Асинхронно получает текущую температуру для города из OpenWeatherMap API.
    Возвращает температуру в градусах Цельсия.
    """
    if not OPENWEATHER_API_KEY:
        # Fallback: generate mock data for demo purposes
        import random

        return round(random.uniform(-10, 35), 1)

    params = {
        "q": city_name,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # Celsius
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            temperature = data.get("main", {}).get("temp")
            return temperature
    except Exception as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None


async def update_all_temperatures(db: AsyncSession) -> Dict[str, Any]:
    """
    Получает текущую температуру для всех городов в БД и сохраняет записи.

    Returns:
        Dict с информацией о результате операции
    """
    cities = await crud.get_cities(db)
    details = []
    successful_updates = 0

    for city in cities:
        temperature = await fetch_temperature_for_city(city.name)

        if temperature is not None:
            temp_create = schemas.TemperatureCreate(
                city_id=city.id, temperature=temperature
            )
            await crud.create_temperature(db, temp_create)
            successful_updates += 1
            details.append(
                {
                    "city_id": city.id,
                    "city_name": city.name,
                    "temperature": temperature,
                    "status": "success",
                }
            )
        else:
            details.append(
                {
                    "city_id": city.id,
                    "city_name": city.name,
                    "status": "failed",
                    "error": "Could not fetch temperature",
                }
            )

    return {
        "message": "Temperature update completed",
        "updated_cities": successful_updates,
        "total_cities": len(cities),
        "details": details,
    }
