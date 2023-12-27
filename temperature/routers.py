import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from dependencies import get_db
from . import schemas, crud

router = APIRouter()
load_dotenv()

BASE_URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("API_KEY")


async def get_temperature_request(db: AsyncSession = Depends(get_db)) -> dict:
    query = select(City)
    cities_list = await db.execute(query)
    cities = [city[0] for city in cities_list.fetchall()]
    information = {}
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {"key": f"{API_KEY}", "q": f"{city.name}"}

            response = await client.get(BASE_URL, params=params)
            weather_data = response.json()
            information[city.id] = weather_data
    return information


@router.get("/update_temperatures/")
async def update_cities_temperature(db: AsyncSession = Depends(get_db)):
    information = await get_temperature_request(db=db)
    return await crud.update_cities_temperature(db=db, information=information)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.TemperatureCity)
async def get_temperature_by_city_id(city_id: int, db: AsyncSession = Depends(get_db)):
    db_temperature = await crud.get_temperature_by_city_id(db=db, city_id=city_id)

    if db_temperature is None:
        return HTTPException(status_code=404, detail="City not found")

    return db_temperature
