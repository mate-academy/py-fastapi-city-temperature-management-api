import asyncio
import os
from datetime import datetime
from typing import List

import httpx
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature_app import crud as temperature_crud
from city_app import crud as city_crud
from temperature_app import schemas

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def read_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    temperatures = await temperature_crud.get_all_temperatures(db, city_id)
    return temperatures


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}"
            )
            response.raise_for_status()
            data = await response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPStatusError as e:
            print(f"HTTP error for {city_name}: {str(e)}")
            raise HTTPException(
                status_code=e.response.status_code, detail=f"Failed to fetch temperature for {city_name}: {str(e)}"
            )
        except Exception as e:
            print(f"General error for {city_name}: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Failed to fetch temperature for {city_name}: {str(e)}"
            )


@router.post(
    "/temperatures/update/", response_model=List[schemas.TemperatureList]
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_all_cities(db)
    temperatures = []

    async def fetch_and_store(city):
        temperature = await fetch_temperature(city.name)
        db_temperature = schemas.TemperatureCreate(
            city_id=city.id, date_time=datetime.now(), temperature=temperature
        )
        return await temperature_crud.create_temperature(db, db_temperature)

    tasks = [fetch_and_store(city) for city in cities]
    temperatures = await asyncio.gather(*tasks)
    return temperatures
