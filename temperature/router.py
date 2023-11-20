import asyncio
from datetime import datetime

from fastapi import Depends, APIRouter
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from settings import settings
from temperature import crud, schemas
from city.models import City
from dependencies import get_db


router = APIRouter()

URL = f"https://api.weatherapi.com/v1/current.json"
PARAMS = {"key": settings.WEATHER_API_KEY}


@router.get("/temperatures/", response_model=list[schemas.TemperatureSerializer])
async def cities_temperature_list(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_temperatures(db=db, skip=skip, limit=limit)


@router.get("/temperatures/{city_id}/", response_model=schemas.TemperatureSerializer)
async def city_temperature_detail(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature_by_city_id(db, city_id=city_id)


@router.post("/temperatures/update/")
async def create_temperature_for_all_cities(
        db: AsyncSession = Depends(get_db)
):
    cities = await get_all_cities(db=db)
    local_parameters = PARAMS

    async with AsyncClient() as client:
        result = []

        for city in cities:
            local_parameters["q"] = city.name
            result.append(
                create_temperature_by_city(
                    db=db,
                    client=client,
                    city=city,
                    local_parameters=local_parameters
                )
            )

        await asyncio.gather(*result)


async def create_temperature_by_city(
        db: AsyncSession,
        client: AsyncClient,
        city: City,
        local_parameters: dict,
) -> None:
    response = await client.get(url=URL, params=local_parameters)
    response = response.json()

    await crud.create_temperature_by_city(
        db=db,
        city_id=city.id,
        date_time=datetime.strptime(response["current"]["last_updated"], "%Y-%m-%d %H:%M"),
        temperature=response["current"]["temp_c"],
    )
