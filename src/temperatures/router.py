from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cities.crud import get_all_cities
from src.dependencies import get_db
from src.exceptions import FetchTemperatureError
from src.temperatures.crud import (
    create_temperatures,
    get_all_temperatures,
    get_temperatures_by_city_id,
)
from src.temperatures.models import DBTemperature
from src.temperatures.schemas import Temperature, TemperatureCreate
from src.temperatures.service import fetch_temperatures_for_all_cities

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperature"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
) -> list[DBTemperature]:
    return await get_all_temperatures(db)


@router.get("/{city_id}", response_model=list[Temperature])
async def read_temperatures_by_city_id(
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[DBTemperature]:
    return await get_temperatures_by_city_id(city_id, db)


@router.post(
    "/update", response_model=list[TemperatureCreate | FetchTemperatureError]
)
async def fetch_temperatures(
    db: AsyncSession = Depends(get_db),
) -> list[TemperatureCreate | FetchTemperatureError]:
    if not (all_cities := await get_all_cities(db)):
        return [
            FetchTemperatureError(
                city_id=None,
                city_name=None,
                code=None,
                message="There are no cities in the database.",
            )
        ]
    cities = [{"id": city.id, "name": city.name} for city in all_cities]
    print(cities)
    temperatures = await fetch_temperatures_for_all_cities(cities)
    await create_temperatures(db, temperatures)
    return temperatures
