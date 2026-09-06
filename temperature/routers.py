import asyncio

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_cities
from dependencies import get_db
from temperature.crud import (
    get_temperatures,
    get_city_temperatures,
    create_temperature
)
from temperature.weather import get_coordinates, get_temperature

router = APIRouter()


@router.get("/temperatures")
async def get_temperatures_endpoint(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
):
    if city_id is None:
        return await get_temperatures(db)

    return await get_city_temperatures(db, city_id)


async def update_city_temperature(city):
    latitude, longitude = await get_coordinates(city.name)
    temperature = await get_temperature(latitude, longitude)

    return city.id, temperature


@router.post("/temperatures/update")
async def update_temperatures(
    db: AsyncSession = Depends(get_db),
):
    cities = await get_cities(db)

    results = await asyncio.gather(
        *(update_city_temperature(city) for city in cities)
    )

    for city_id, temperature in results:
        await create_temperature(db, city_id, temperature)

    return {"message": "Temperatures updated"}
