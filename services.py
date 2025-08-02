import os
import aiohttp
from datetime import datetime
from crud import get_cities, create_temperature
from database import get_db
from fastapi import HTTPException


async def fetch_weather_data(city_name: str):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenWeatherMap API key not configured"
        )

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status != 200:
                return None
            data = await response.json()
            return data.get("main", {}).get("temp")


async def update_all_temperatures(db: Session):
    cities = get_cities(db)
    results = []

    for city in cities:
        try:
            temp = await fetch_weather_data(city.name)
            if temp is not None:
                temp_record = schemas.TemperatureCreate(
                    city_id=city.id,
                    temperature=temp,
                    date_time=datetime.utcnow()
                )
                create_temperature(db, temp_record)
                results.append({"city": city.name, "status": "success"})
            else:
                results.append({"city": city.name, "status": "failed"})
        except Exception:
            results.append({"city": city.name, "status": "error"})

    return results
