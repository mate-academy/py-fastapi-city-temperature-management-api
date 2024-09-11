from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import CommonDB, CommonLimitation
from temperature.crud import (
    get_temperature,
    get_temperature_by_city,
    updates_temperature,
)
from temperature.schemas import Temperature
from temperature.utils import weather_message

router = APIRouter()


@router.get("/temperatures/", response_model=List[Temperature])
async def get_temperatures(
        db: CommonDB,
        params_limit: CommonLimitation
) -> list[Temperature]:
    return await get_temperature(db=db, **params_limit)


@router.get("/temperatures/{city_id}/", response_model=List[Temperature])
async def get_temperature_by_city_id(
        db: CommonDB,
        city_id: int,
        params_limit: CommonLimitation
) -> list[Temperature]:
    temperature = await get_temperature_by_city(
        db=db,
        city_id=city_id,
        **params_limit
    )

    if len(temperature) == 0:
        raise HTTPException(
            status_code=404, detail="There is no data for this city"
        )

    return temperature


@router.post("/temperatures/update/")
async def update_temperature(db: CommonDB) -> dict:
    invalid_cities, valid_cities = await updates_temperature(db=db)
    message = weather_message(
        invalid_cities=invalid_cities,
        valid_cities=valid_cities
    )

    return {"message": message}
