import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.models import City
from dependencies import get_db
from temperature import schemas, crud
from temperature.utils import fetch_temperature

router = APIRouter()


@router.post("/temperatures/", response_model=list[schemas.Temperature])
def create_temperatures(db: Session = Depends(get_db)):
    сities = db.query(City).all()

    for city in сities:
        city_temperature = asyncio.run(fetch_temperature(city.name))
        temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=city_temperature
        )
        db_temperature = crud.get_temperature_by_city_id(
            db=db,
            city_id=city.id
        )
        if db_temperature:
            crud.update_temperature_by_id(
                db=db,
                temperature=temperature,
                temperature_id=db_temperature.id
            )
        else:
            crud.create_temperature(
                db=db,
                temperature=temperature
            )

    return crud.get_all_temperatures(db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.Temperature)
def read_temperature_by_city_id(city_id: int, db: Session = Depends(get_db)):
    db_temperature = crud.get_temperature_by_city_id(db=db, city_id=city_id)

    if db_temperature is None:
        raise HTTPException(
            status_code=400,
            detail="Such city_id for Temperature not found"
        )

    return db_temperature
