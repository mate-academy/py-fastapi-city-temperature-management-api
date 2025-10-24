# services/temperature_service.py
import asyncio
import httpx
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_CRUD import models
from .models import Temperature
from city_CRUD.models import City

API_KEY = "APIKEY"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_coordinates(client: httpx.AsyncClient, city_name: str):
    """Fetch lat/lon for a given city name."""
    params = {"q": city_name, "limit": 1, "appid": API_KEY}
    r = await client.get(GEOCODE_URL, params=params)
    r.raise_for_status()
    data = r.json()
    if not data:
        return None, None
    lat, lon = data[0]["lat"], data[0]["lon"]
    return lat, lon


async def fetch_temperature(client: httpx.AsyncClient, lat: float, lon: float):
    """Fetch current temperature for coordinates."""
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    r = await client.get(WEATHER_URL, params=params)
    r.raise_for_status()
    data = r.json()
    return data["main"]["temp"]


async def update_all_temperatures(session: AsyncSession):
    """
    Fetch temperatures for all cities and store a historical record for each.
    Each fetch creates a new Temperature record with timestamp.
    """
    result = await session.execute(select(City))
    cities = result.scalars().all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            lat, lon = await fetch_coordinates(client, city.name)
            if lat is None or lon is None:
                print(f"⚠️ Could not fetch coordinates for {city.name}")
                continue

            temp = await fetch_temperature(client, lat, lon)

            new_entry = Temperature(
                city_id=city.id,
                temperature=temp,
                date_time=datetime.utcnow()
            )
            session.add(new_entry)
            print(f"🕒 Recorded {temp}°C for {city.name} at {new_entry.date_time} UTC.")

        await session.commit()
        print("✅ All city temperatures recorded to history.")
