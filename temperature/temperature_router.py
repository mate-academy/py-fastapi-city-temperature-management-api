import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import models
from temperature import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperature(db: Session = Depends(get_db)):
    for city in db.query(models.City).all():
        try:
            await crud.fetch_temperatures(db=db, city=city)
        except KeyError:
            continue
    return {"message": "Temperatures were successfully updated"}


@router.get("/temperatures/{city_id}", response_model=List[schemas.TemperatureList])
def read_temperature_for_city(
        city_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    temperature = crud.get_temperature_by_city_id(db, city_id, skip, limit)
    return temperature


@router.get("/temperatures", response_model=list[schemas.TemperatureList])
def read_temperature(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    temperatures = crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures
