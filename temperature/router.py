from typing import List

from fastapi import APIRouter, HTTPException

from city.dependencies import CommonParametersWithId
from dependencies import CommonDB, CommonLimitation

from temperature import crud, schemas
from temperature.utils import generate_main_message


router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: CommonDB):
    invalid_cities, valid_cities = await crud.update_temperatures(db)
    message = generate_main_message(
        invalid_cities=invalid_cities,
        valid_cities=valid_cities
    )

    return {"message": message}


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
        params_db: CommonDB,
        params_limit: CommonLimitation
):
    return await crud.get_temperatures(db=params_db, **params_limit)


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
async def get_temperature_by_city_id(
        params_db: CommonDB,
        params_id: CommonParametersWithId
):
    temperature = await crud.get_temperature_by_city_id(
        db=params_db,
        city_id=params_id
    )

    if temperature is None:
        raise HTTPException(
            status_code=404,
            detail="Temperature for this city doesn't exist"
        )
    return temperature
