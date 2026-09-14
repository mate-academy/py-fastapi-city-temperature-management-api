from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    get_cities,
    get_city,
    create_city,
    delete_city,
    create_temperature,
    get_temperatures,
)
from app.dependencies import get_db
from app.schemas import CityList, CityCreate, TemperatureList
from app.services.weather import (
    fetch_current_temperature_by_city_name,
    WeatherServiceError,
)

router = APIRouter()


@router.get("/cities/", response_model=List[CityList])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await get_cities(db=db)


@router.get("/cities/{id}", response_model=CityList)
async def read_city(id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city(
        city_id=id,
        db=db,
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city


@router.post("/cities/", response_model=CityList)
async def new_city(city_data: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_city(city_data=city_data, db=db)


@router.delete("/cities/{id}")
async def delete_city_view(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    city = await get_city(
        city_id=id,
        db=db,
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    await delete_city(
        city=city,
        db=db,
    )


@router.post("/temperatures/update", response_model=List[TemperatureList])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db=db)
    city_data = [(city.id, city.name) for city in cities]

    created = []
    for city_id, city_name in city_data:
        try:
            temp = await fetch_current_temperature_by_city_name(city_name)
        except WeatherServiceError:
            continue
        record = await create_temperature(
            db=db,
            city_id=city_id,
            date_time=datetime.now(timezone.utc),
            temperature=temp,
        )
        created.append(TemperatureList.model_validate(record))

    return created


@router.get("/temperatures", response_model=List[TemperatureList])
async def read_temperatures(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
):
    return await get_temperatures(db=db, city_id=city_id)
