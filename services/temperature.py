from datetime import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TemperatureModel, CityModel

API_KEY = "d2e6157f5c84475389d73858252907"
URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_temperature(city_name: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{URL}?q={city_name}&key={API_KEY}")
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Error fetching data for {city_name}: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to fetch temperature for {city_name}: {e.response.text}"
            )

        data = response.json()

        if "current" not in data or "temp_c" not in data["current"]:
            raise HTTPException(
                status_code=404,
                detail=f"Temperature data not found for {city_name}"
            )

        return float(data["current"]["temp_c"])


async def update_temperatures(db: AsyncSession) -> int:
    result = await db.execute(select(CityModel))
    cities = result.scalars().all()

    cities_updated = 0
    for city in cities:
        temp_value= await fetch_temperature(city.name)
        new_temp_obj = TemperatureModel(
            city_id=city.id,
            temperature=temp_value,
            date_time=datetime.utcnow()
        )
        db.add(new_temp_obj)
        cities_updated += 1

    await db.commit()
    return cities_updated


async def get_temperatures(db: AsyncSession, city_id: int) -> list[TemperatureModel]:
    query = select(TemperatureModel)
    if city_id is not None:
        query = query.where(TemperatureModel.city_id == city_id)
    result = await db.execute(query)

    temperatures = result.scalars().all()
    return temperatures


async def get_temperature(temp_id: int, db: AsyncSession) -> TemperatureModel:
    result = await db.execute(select(TemperatureModel).where(TemperatureModel.id == temp_id))

    temperature = result.scalar_one_or_none()
    if not temperature:
        raise HTTPException(
            status_code=404,
            detail="Object not found"
        )

    return temperature
