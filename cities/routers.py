import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cities import weather_service
from cities.crud import (
    get_city_by_id,
    get_temperatures,
    get_temperatures_for_city,
    temperatures_create,
    city_create,
    get_cities,
    city_update,
    city_delete,
)
from cities.schemas import (
    Temperature,
    City,
    CityCreate,
    CityUpdate
)
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=City)
async def create_city(
    city: CityCreate,
    db: AsyncSession = Depends(get_db)
) -> City:
    return await city_create(db=db, city=city)


@router.get("/cities/", response_model=list[City])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> list[City]:
    return await get_cities(db=db)


@router.get("/cities/{city_id}", response_model=City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)) -> City:
    city = await get_city_by_id(db=db, city_id=city_id)

    return city


@router.put("/cities/{city_id}", response_model=City)
async def update_city(
    city_id: int,
    update_data: CityUpdate,
    db: AsyncSession = Depends(get_db)
) -> City:
    city = await city_update(
        db=db,
        city_id=city_id,
        update_data=update_data
    )

    return city


@router.delete("/cities/{city_id}", response_model=str)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> str:
    city = await get_city_by_id(db=db, city_id=city_id)

    return await city_delete(db=db, city=city)


@router.get("/temperatures/", response_model=list[Temperature])
async def get_all_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db)
) -> list[Temperature]:
    if city_id is None:
        return await get_temperatures(db=db)

    temperatures = await (
        get_temperatures_for_city(db=db, city_id=city_id)
    )

    return temperatures


@router.post("/temperature/update/", response_model=str)
async def update_temperatures_for_all_cities(
    db: AsyncSession = Depends(get_db),
) -> str:
    all_cities = await get_all_cities(db=db)
    weathers = [
        weather_service.fetch_weather(
            city_name=city.name,
        )
        for city in all_cities
    ]
    temperatures = await asyncio.gather(*weathers)
    new_temperatures_data = [
        {"city_id": city.id, "temperature": temperatures[index]}
        for index, city in enumerate(all_cities)
        if temperatures[index] is not None
    ]
    return await temperatures_create(db, new_temperatures_data)
