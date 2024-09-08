import os

import httpx
from datetime import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from city_crud_api.crud import get_cities
from dependencies import get_db, pagination_params
from city_crud_api import schemas, crud


load_dotenv()


class Settings(BaseSettings):
    weather_api_key: str = os.getenv("WEATHER_API_KEY")

settings = Settings()

router = APIRouter()


@router.get("/temperatures/", response_model=List[schemas.TemperatureList])
async def read_temperatures(
        pagination: tuple[int, int] = Depends(pagination_params),
        db: AsyncSession = Depends(get_db)
):
    skip, limit = pagination
    temperatures = await crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures


@router.get("/temperatures/by-city/", response_model=List[schemas.TemperatureList])
async def read_temperatures_by_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    temperatures = await crud.get_temperatures_by_city(db, city_id=city_id)
    return temperatures


@router.post("/temperatures/update", response_model=List[schemas.TemperatureList])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)
    updated_temperatures = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(
                f"http://api.weatherapi.com/v1/current.json?key={settings.weather_api_key}&q={city.name}")
            data = response.json()
            temperature = data["current"]["temp_c"]
            temp_create = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature
            )
            updated_temperature = await crud.create_temperature(db, temp_create)
            updated_temperatures.append(updated_temperature)

    return updated_temperatures
