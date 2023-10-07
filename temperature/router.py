import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud
import httpx
from dotenv import load_dotenv
from city.models import DBCity as DBCITY

load_dotenv()
API_KEY = os.getenv("API_KEY")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?"
router = APIRouter()


async def get_temperature_request(db):
    query = select(DBCITY)
    cities_list = await db.execute(query)
    cities = [city[0] for city in cities_list.fetchall()]
    information = {}
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {
                "q": city.name,
                "units": "metric",
                "appid": API_KEY
            }

            response = await client.get(WEATHER_URL, params=params)
            weather_data = response.json()
            information[city.id] = weather_data
    return information


@router.post("/temperatures/update/")
async def update_temperature(db: AsyncSession = Depends(get_db)):
    information = await get_temperature_request(db=db)
    return await crud.update_temperature(db=db, information=information)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_city(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.TemperatureCity)
async def read_single_temperatures_by_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_temperature_by_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail=city_id)

    return db_city
