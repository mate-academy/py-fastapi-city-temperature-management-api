
from fastapi import APIRouter

from dependencies import CommonLimits, CommonDB
from . import crud, schemas
from .crud import update_all_temperatures, update_single_city_temperature

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def list_of_all_temperatures(db: CommonDB, limits: CommonLimits) -> list[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db, **limits)


@router.get("/temperatures/{city_id}/", response_model=list[schemas.Temperature])
async def list_of_city_temperatures(
        city_id: int,
        db: CommonDB,
        limits: CommonLimits
) -> list[schemas.Temperature]:
    return await crud.get_city_temperatures(db=db, city_id=city_id, **limits)


@router.post("/temperatures/update/{city_id}/", response_model=schemas.Temperature)
async def update_city_temperature(city_id: int, db: CommonDB) -> schemas.Temperature:
    return await update_single_city_temperature(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=dict)
async def update_temperatures(db: CommonDB) -> dict:
    return await update_all_temperatures(db=db)
