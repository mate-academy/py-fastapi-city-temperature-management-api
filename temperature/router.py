import os
from datetime import datetime
from typing import List, Annotated

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
import httpx

from city import models
from dependencies import get_db
from temperature import schemas, crud
from utils import general_parameter

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(
        db: AsyncSession = Depends(get_db)
) -> dict:
    cities_result = await db.execute(select(models.City))
    cities = cities_result.scalars().all()

    async with httpx.AsyncClient() as client:
        temperature_list = []
        for city in cities:
            params = {
                "key": API_KEY,
                "q": city.name
            }
            response = await client.get(
                url=WEATHER_API_URL,
                params=params
            )
            if response.status_code == 200:
                weather_dict = response.json()
                temperature_create = schemas.TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.now(),
                    temperature=weather_dict["current"]["temp_c"]
                )
                temperature_list.append(temperature_create)

        for temperature in temperature_list:
            await crud.create_temperature(db=db, temperature=temperature)

    return {"message": "Temperature data updated"}


@router.get("/temperatures/")
async def get_all_temperatures(
        general: Annotated[dict, Depends(general_parameter)]
) -> List[schemas.TemperatureBase]:
    temperatures = await crud.get_all_temperatures(**general)
    return temperatures


@router.get("/temperatures/{city_id}/")
async def get_temperatures_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.TemperatureList:
    db_city = await crud.get_temperatures_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail=f"Temperature with city id = {city_id} not found"
        )

    return db_city
