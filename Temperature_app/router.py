import asyncio
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from project_settings.dependecies import get_db
from . import schemas, crud
from City_app.crud import get_all_cities
from City_app.schemas import City
from .utils import update_city_temperature

temperature_router = APIRouter()


@temperature_router.get(
    path="/temperatures",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Temperature]
)
async def get_temperatures(
    db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db)


@temperature_router.get(
    path="/temperatures/?city_id={city_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Temperature]
)
async def get_temperature_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    return await crud.get_temperature_by_city_id(
        db=db,
        city_id=city_id
    )


@temperature_router.get(
    path="/temperatures/update",
    status_code=status.HTTP_201_CREATED,
    response_model=List[City]
)
async def temperatures_update(
        db: AsyncSession = Depends(get_db)
) -> List[City]:
    cities = await get_all_cities(db=db)
    tasks = []
    for city in cities:
        tasks.append(update_city_temperature(city))

    cities_schema_list = await asyncio.gather(*tasks)
    return list(cities_schema_list)
