import os
from datetime import datetime

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city_temperature.schemas import (
    City,
    CityCreate,
    CityUpdate,
    TemperatureCreate,
    Temperature,
)
from city_temperature import crud

router = APIRouter()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


@router.post("/cities/", response_model=City)
def create_city(
    city: CityCreate,
    db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/cities/{city_id}/", response_model=City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=City)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.delete_city(db=db, city_id=city_id)


@router.post("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    async with aiohttp.ClientSession() as session:
        cities = crud.get_cities(db=db)
        for city in cities:
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&APPID={WEATHER_API_KEY}&units=metric"
            ) as response:
                data = await response.json()
                temperature = data["temperature"]
                temp_record = TemperatureCreate(
                    city_id=city.id, date_time=datetime.now(), temperature=temperature
                )
                crud.create_temperature(db=db, temperature=temp_record)
    return {"detail": "Temperatures updated"}


@router.get("/temperatures/", response_model=list[Temperature])
def read_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db)


@router.get("/temperatures/?city_id={city_id}/", response_model=list[Temperature])
def read_temperatures_by_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperatures_by_city_id(db=db, city_id=city_id)
