from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import DBCity
from app.dependencies import get_session
from app.temperature import schemas
from app.temperature.crud import (
    create_temp_record,
    get_all_temp,
    get_temp_for_city
)
from app.temperature.models import DBTemperature
from app.temperature.weather import fetch_temperature_data

router = APIRouter(tags=["Temperature"])


@router.post("/update/", response_model=list[schemas.TemperatureUpdate])
async def temp_update(
        db: AsyncSession = Depends(get_session)
) -> [DBTemperature]:
    cities_result = await db.execute(select(DBCity))
    cities = cities_result.scalars().all()
    updated_cities = []

    for city in cities:
        temp = await fetch_temperature_data(city.city)
        created_entry = await create_temp_record(
            city_id=city.id, temp=temp, db=db)
        updated_cities.append({
            "city_id": created_entry.city_id,
            "temperature": created_entry.temperature,
            "date_time": created_entry.date_time
        })

    return updated_cities


@router.get("/", response_model=list[schemas.TemperatureRead])
async def read_all_temperatures(
        db: AsyncSession = Depends(get_session)
) -> [DBTemperature]:
    return await get_all_temp(db=db)


@router.get("/{city_id}/", response_model=list[schemas.TemperatureRead])
async def read_temp_for_city(
        city_id: int,
        db: AsyncSession = Depends(get_session)
) -> DBTemperature:
    return await get_temp_for_city(id_city=city_id, db=db)
