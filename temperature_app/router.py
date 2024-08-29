from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import httpx
from datetime import datetime

from city_app import crud as city_crud
from dependencies import get_db
from temperature_app import schemas, crud
from settings import settings

router = APIRouter()


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def read_temperatures(
    city_id: int = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    temperatures = await crud.get_temperatures_list(
        db, skip=skip, limit=limit, city_id=city_id
    )
    return temperatures


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_cities_list(db)

    async with httpx.AsyncClient() as client:
        schema_temperatures = []
        for city in cities:
            response = await client.get(
                f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={city.name}"
            )
            data = response.json()
            city_temperature = data["current"]["temp_c"]
            schema_temperature = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=city_temperature,
            )
            schema_temperatures.append(schema_temperature)

    return await crud.create_temperatures(db, schema_temperatures)
