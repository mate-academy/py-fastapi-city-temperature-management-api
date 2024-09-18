import asyncio
import os
from datetime import datetime
from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from temperature import crud, schemas
from db.engine import get_db

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

router = APIRouter(tags=["temperatures"])


class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://api.weatherapi.com/v1/current.json?key="
                f"{API_KEY}&q={city_name}"
            )
            response.raise_for_status()
            data = response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching temperature: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Request error when fetching temperature: {str(e)}"
            )
        except httpx.TimeoutException as e:
            raise HTTPException(
                status_code=504,
                detail=f"Timeout error when fetching temperature: {str(e)}"
            )


@router.get("/", response_model=List[schemas.Temperature])
async def fetch_all_temperatures(
        pagination: PaginationParams = Depends(),
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    temperatures = await crud.get_temperatures(db, skip=pagination.skip, limit=pagination.limit)
    return temperatures


@router.get("/cities/{city_id}/", response_model=List[schemas.Temperature])
async def fetch_temperatures_by_city(
        city_id: int,
        pagination: PaginationParams = Depends(),
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    temperatures = await crud.get_temperature_by_city(
        db, city_id=city_id, skip=pagination.skip, limit=pagination.limit
    )
    return temperatures


@router.post("/update/", response_model=List[schemas.Temperature])
async def update_temperatures(
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    cities = await crud.get_cities(db)
    temperatures = []

    async def fetch_and_store(city) -> schemas.Temperature:
        temperature = await fetch_temperature(city.name)
        db_temperature = schemas.TemperatureCreate(
            city_id=city.id, date_time=datetime.now(), temperature=temperature
        )
        return await crud.create_temperature(db, db_temperature)

    tasks = [fetch_and_store(city) for city in cities]
    temperatures = await asyncio.gather(*tasks)
    return temperatures
