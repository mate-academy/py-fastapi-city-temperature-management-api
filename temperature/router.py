from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List

from temperature import crud
from temperature.schemas import TemperatureList, TemperatureBase
from dependencies import get_db


router = APIRouter()


@router.get("/temperatures/", response_model=List[TemperatureList])
def get_all_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db)


@router.get("/temperatures/{city_id}/", response_model=TemperatureBase)
def get_temperature_by_city_id(city_id: int, db: Session = Depends(get_db)):
    db_temperature = crud.get_temperature_by_city_id(city_id=city_id, db=db)
    if db_temperature:
        return db_temperature

    raise HTTPException(
        status_code=404, detail=f"City with id {city_id} not found"
    )


@router.put("/temperatures/update/", response_model=List[TemperatureList])
async def update_temperatures(db: Session = Depends(get_db)):
    return await crud.update_all_temperatures(db)
