import asyncio
from os import environ

from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, insert

from dependencies import AsyncDB
from httpx import AsyncClient

from src.City.models import City
from src.Temperature.models import Temperature
from src.Temperature import schemas, crud
from src.config import settings

router = APIRouter()


async def get_temperature_data(city_name: str, city_id: int, client: AsyncClient) -> tuple[dict, int]:
    res = await client.get(
        settings.WEATHER_API_BASE_URL,
        params={"key": environ["WEATHER_API_KEY"], "q": city_name},
    )
    return res.json()["current"]["temp_c"], city_id


@router.post("/update")
async def update_city(db: AsyncDB):
    result = (
        await db.execute(select(City.name, City.id))
    ).all()

    async with AsyncClient() as client:
        tasks = (
            get_temperature_data(city_name=city_name, city_id=city_id, client=client)
            for city_name, city_id in result
        )
        results = await asyncio.gather(*tasks)

    bulk_objects = (
        {
            "city_id": city_id,
            "temperature": city_temp,
        }
        for city_temp, city_id in results
    )
    await db.execute(
        insert(Temperature),
        bulk_objects
    )
    await db.commit()


@router.get("/", response_model=List[schemas.TemperatureRead])
async def get_all_temperatures(db: AsyncDB):
    return await crud.get_all_temperatures(db=db)


@router.get("/{city_id}", response_model=List[schemas.TemperatureRead])
async def get_temperatures_by_city_id(db: AsyncDB, city_id: int):
    return await crud.get_all_temperatures_by_city_id(db=db, city_id=city_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
