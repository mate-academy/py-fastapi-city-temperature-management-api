import asyncio
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from city import crud
from city.models import CityModels
from temperature_api.crud import get_temperatures_by_city_id
from temperature_api.models import TemperatureModels
from temperature_api.schemas import Temperature, TemperatureCreate
from temperature_api.weather_get import get_weather
from dependencies import get_db
from temperature_api import crud, schemas

router = APIRouter()


@router.get("/temperature/", response_model=list[schemas.Temperature])
async def read_all_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperature(db=db)


@router.post("/temperature/", response_model=schemas.Temperature)
async def create_new_temperature(
        temperature_data: schemas.TemperatureCreate,
        db: AsyncSession = Depends(get_db)
):
    # Get the city name from the request
    city_name = await crud.get_city_name_by_id(db=db, city_id=temperature_data.city_id)

    if city_name is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Fetch weather data for the city
    temperature = get_weather(city_name)

    if temperature is None:
        raise HTTPException(status_code=404, detail="Weather data unavailable")

    # Update the temperature object with the retrieved data
    temperature_data.temperature = temperature

    return await crud.create_temperature(db=db, temperature=temperature_data)


@router.get("/temperature/?city_id={city_id}")
async def get_temperatures(city_id: int):
    temperatures = await get_temperatures_by_city_id(city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures found for this city.")
    return temperatures


@router.post("/temperatures/update", response_model=List[Temperature])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await db.execute(select(CityModels))
    cities = cities.scalars().all()

    temperatures_data = []

    async def fetch_temperature(city_name: str):
        try:
            temperature = await get_weather(city_name)
            city = await db.execute(select(CityModels).where(CityModels.name == city_name))
            city = city.scalar_one_or_none()

            if city:
                temperature_data = TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.utcnow(),
                    temperature=temperature
                )
                temperatures_data.append(temperature_data)
            else:
                print(f"City '{city_name}' not found in the database.")
        except ValueError as ve:
            print(f"Error fetching temperature data for {city_name}: {ve}")

    tasks = [fetch_temperature(city.name) for city in cities]
    await asyncio.gather(*tasks)

    db_temperatures = [
        TemperatureModels(**data.model_dump()) for data in temperatures_data
    ]

    # Use the add_all() method of AsyncSession to add the list of temperatures
    db.add_all(db_temperatures)

    # Use the commit() method of AsyncSession to commit the changes
    await db.commit()

    # Use the refresh() method of AsyncSession to refresh the temperature objects with the database state
    for temp in db_temperatures:
        await db.refresh(temp)

    return db_temperatures
