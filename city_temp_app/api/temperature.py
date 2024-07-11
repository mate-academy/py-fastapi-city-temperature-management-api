from datetime import datetime

import httpx

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from city_temp_app.api.city import router
from city_temp_app import schemas, crud
from city_temp_app.database import get_db
from city_temp_app.models import Temperature


WEATHER_API_URL = "http://api.weatherapi.com/v1"


client = httpx.AsyncClient()


@router.post(
    "/temperatures/update/", response_model=list[schemas.Temperature]
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud.read_cities(db)
    temperatures = []
    try:
        for city in cities:
            response = await client.get(
                f"{WEATHER_API_URL}/weather?city={city.name}"
            )
            if response.status_code == 200:
                temp_data = response.json()
                temperature = schemas.TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.now(),
                    temperature=temp_data['temperature']
                )
                db_temperature = await crud.create_temperature(
                    db, temperature
                )
                temperatures.append(db_temperature)
    finally:
        return temperatures


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    return await crud.read_temperatures(db=db)


@router.get(
    "/temperatures/{city_id}/", response_model=schemas.Temperature
)
async def read_temperatures_by_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> Temperature:
    return await crud.read_temperatures(db=db, city_id=city_id)
