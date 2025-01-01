import os
import httpx

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from datetime import datetime
from dotenv import load_dotenv

from temperature_api import models, schemas
from city_crud_api.models import City

from dependencies import get_db
from city_crud_api.crud import get_all_cities

load_dotenv()


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    try:
        city_query = select(City).where(City.id == temperature.city_id)
        city_result = await db.execute(city_query)
        city = city_result.scalar()

        if not city:
            raise HTTPException(status_code=400, detail=f"City with ID {temperature.city_id} not found!")

        query = (
            insert(models.Temperature)
            .values(
                city_id=temperature.city_id,
                date_time=temperature.date_time,
                temperature=temperature.temperature,
            )
            .returning(models.Temperature.id)
        )
        result = await db.execute(query)
        temperature_id = result.scalar_one()

        await db.commit()

        return {
            **temperature.dict(),
            "id": temperature_id,
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create temperature record.")


async def update_temperature(db: AsyncSession = Depends(get_db)):
    API_WEATHER = os.getenv("API_WEATHER")
    if not API_WEATHER:
        raise HTTPException(status_code=500, detail="Weather API key is not configured.")

    API_URL = "https://api.weatherapi.com/v1/current.json"
    try:
        cities = await get_all_cities(db)
        if not cities:
            raise HTTPException(status_code=404, detail="No city found!")

        updated_temperatures = []

        async with httpx.AsyncClient() as client:
            for city in cities:
                try:
                    response = await client.get(
                        API_URL,
                        params={
                            "key": API_WEATHER,
                            "q": city.name
                        },
                        timeout=10
                    )
                    response.raise_for_status()

                    data = response.json()
                    if "current" not in data or "temp_c" not in data["current"]:
                        raise HTTPException(status_code=502, detail="Invalid response structure from weather API.")

                    current_temperature = data["current"]["temp_c"]

                    query = select(models.Temperature).where(models.Temperature.city_id == city.id)
                    result = await db.execute(query)
                    existing_temperature = result.scalar_one_or_none()

                    if existing_temperature:
                        update_query = (
                            update(models.Temperature)
                            .where(models.Temperature.city_id == city.id)
                            .values(
                                date_time=datetime.utcnow(),
                                temperature=current_temperature
                            )
                        )
                        await db.execute(update_query)

                        updated_temperatures.append({
                            "city_id": city.id,
                            "date_time": datetime.utcnow(),
                            "temperature": current_temperature
                        })
                    else:
                        insert_query = insert(models.Temperature).values(
                            city_id=city.id,
                            date_time=datetime.utcnow(),
                            temperature=current_temperature
                        ).returning(models.Temperature.id)
                        result = await db.execute(insert_query)
                        temperature_id = result.scalar_one()

                        updated_temperatures.append({
                            "id": temperature_id,
                            "city_id": city.id,
                            "date_time": datetime.utcnow(),
                            "temperature": current_temperature
                        })
                except httpx.RequestError:
                    updated_temperatures.append({
                        "city_id": city.id,
                        "error": f"Failed to fetch temperature for city {city.name} due to HTTP error."
                    })
                except Exception:
                    updated_temperatures.append({
                        "city_id": city.id,
                        "error": f"An unexpected error occurred while updating city {city.name}."
                    })

        await db.commit()

        return updated_temperatures
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update temperatures.")


async def get_temperature(db: AsyncSession = Depends(get_db)):
    try:
        query = select(models.Temperature)
        result = await db.execute(query)
        temperature = result.scalars().all()
        return temperature
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch temperatures.")


async def get_temperature_by_city_id(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(models.Temperature).where(models.Temperature.city_id == city_id)
        result = await db.execute(query)
        temperature = result.scalar_one_or_none()
        if not temperature:
            raise HTTPException(status_code=404, detail=f"No temperature records found for city ID {city_id}.")
        return temperature
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch temperature for the specified city.")
