import httpx
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Temperature


async def geocode_city(city_name: str) -> Optional[Tuple[float, float]]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params={"name": city_name, "count": 1})
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                return result["latitude"], result["longitude"]
        except httpx.HTTPError:
            return None
    return None


async def fetch_current_temperature(lat: float, lon: float) -> Optional[float]:
    url = "https://api.open-meteo.com/v1/forecast"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                url,
                params={"latitude": lat, "longitude": lon, "current_weather": "true"},
            )
            response.raise_for_status()
            data = response.json()
            if "current_weather" in data:
                return float(data["current_weather"]["temperature"])
        except httpx.HTTPError:
            return None
    return None


async def update_temperatures_for_cities(cities: list, db: AsyncSession) -> list[Temperature]:
    new_records = []
    for city in cities:
        coords = await geocode_city(city.name)
        if not coords:
            continue

        lat, lon = coords
        temp_val = await fetch_current_temperature(lat, lon)
        if temp_val is not None:
            temp_record = Temperature(city_id=city.id, temperature=temp_val)
            db.add(temp_record)
            new_records.append(temp_record)

    await db.commit()
    for record in new_records:
        await db.refresh(record)

    return new_records
