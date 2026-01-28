from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sentry_sdk.session import Session
from sqlalchemy import select

import schemas
from crud import get_all_temperatures, get_temperatures_by_city, \
    get_city_by_id, create_temperature
from dependencies import get_db
from models import City
from schemas import TemperatureCreate
from service import fetch_temperature

router = APIRouter()


@router.get("/temperatures/", tags=["temperatures"],
            response_model=list[schemas.TemperatureRead])
def read_temperatures(db: Annotated[Session, Depends(get_db)]):
    return get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=list[schemas.TemperatureRead])
def read_city_temperature(
        city_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    return get_temperatures_by_city(db, city_id)


@router.post("/temperatures/", response_model=schemas.TemperatureCreate)
def temperature_create(
        temperature: schemas.TemperatureCreate,
        db: Annotated[Session, Depends(get_db)]
):
    db_city = get_city_by_id(db=db, city_id=temperature.city_id)
    if not db_city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return create_temperature(db, temperature)


@router.post("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.scalars(select(City)).all()

    for city in cities:
        temp = await fetch_temperature(city.name)

        create_temperature(
            db,
            TemperatureCreate(
                city_id=city.id,
                temperature=temp
            )
        )

    return {"status": "temperatures updated"}
