import asyncio
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city.crud import get_cities
from dependencies import get_db
from temp_aquirer import get_weather_async
from temperature import schemas, crud, models

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"]
)


async def fetch_temperature_for_city(city_id: int, city_name: str):
    try:
        weather_data = await get_weather_async(city_name)
        temp_c = weather_data["current"]["temp_c"]
        return city_id, temp_c, None
    except Exception as e:
        return city_id, None, e


@router.post(
    "/update",
    response_model=list[schemas.Temperature],
    summary="Update temperatures for cities in database"
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)

    city_infos = [(city.id, city.name) for city in cities]

    results = await asyncio.gather(
        *(fetch_temperature_for_city(
            city_id, city_name
        ) for city_id, city_name in city_infos)
    )

    temperatures = []

    for city_id, temp_c, error in results:
        if error:
            print(f"Error fetching weather for city '{city_id}': {error}")
            continue
        temp_create = schemas.TemperatureCreate(
            city_id=city_id,
            date_time=datetime.now(),
            temperature=temp_c
        )
        await crud.create_temperature(db, temp_create)

        stmt = (
            select(models.DBTemperature)
            .options(selectinload(models.DBTemperature.city))
            .where(models.DBTemperature.city_id == city_id)
            .order_by(models.DBTemperature.date_time.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        db_temp = result.scalar_one_or_none()

        if db_temp:
            temperatures.append(schemas.Temperature.model_validate(db_temp))
    return temperatures


@router.get(
    "/",
    response_model=list[schemas.Temperature],
    include_in_schema=True,
    summary="Get temperatures, optionally filtered by city_id",
    tags=["temperatures"]
)
async def list_temperatures(
    city_id: Optional[int] = Query(
        None, description="Filter temperatures by city ID"
    ),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db=db, city_id=city_id)
