from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import ComDB, ComLimitation

from temperature import crud, schemas
from temperature.get_temperature import response_message

router = APIRouter()


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
        db: ComDB,
        params_limit: ComLimitation
) -> list[schemas.Temperature]:
    return await crud.get_temperature(db=db, **params_limit)


@router.get("/temperatures/{city_id}/", response_model=List[schemas.Temperature])
async def get_temperature_by_city_id(
        db: ComDB,
        city_id: int,
        params_limit: ComLimitation
) -> list[schemas.Temperature]:
    temperature = await crud.get_temperature_by_city(
        db=db,
        city_id=city_id,
        **params_limit
    )

    if len(temperature) == 0:
        raise HTTPException(
            status_code=404, detail="Temperature for this city doesn't exist"
        )

    return temperature


@router.post("/temperatures/update/")
async def update_temperature(db: ComDB) -> dict:
    invalid_cities, valid_cities = await crud.updates_temperature(db=db)
    message = response_message(
        invalid_cities=invalid_cities,
        valid_cities=valid_cities
    )

    return {"message": message}
