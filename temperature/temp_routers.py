from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from temperature import temp_schemass
from db import database
from temperature.temp_crud import (
    get_all_temperatures,
    get_one_temperature_by_city_id,
    update_all_temperatures,
)


router = APIRouter(
    tags=["Temperatures"],
    prefix="/temperatures"
)


@router.put("/update/")
async def update_temperatures(db: Session = Depends(database.get_db)):
    return await update_all_temperatures(db=db)


@router.get(
    "/",
    response_model=List[temp_schemass.Temperature]
)
async def get_temperatures(db: Session = Depends(database.get_db)):
    return await get_all_temperatures(db=db)


@router.get("/{city_id}/")
async def get_temperature_by_city(
        city_id: int,
        db: Session = Depends(database.get_db)
):
    return await get_one_temperature_by_city_id(city_id=city_id, db=db)
