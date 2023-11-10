from datetime import datetime

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from settings import settings
from city.crud import get_all_cities
from temperature import schemas, crud


router = APIRouter()

BASE_URL = f"https://api.weatherapi.com/v1/current.json"
parameters = {"WEATHER_API_KEY": settings.WEATHER_API_KEY}


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
def read_temperatures(db: Session = Depends(get_db)) -> list[schemas.TemperatureList]:
    return crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.TemperatureList)
def read_temperature_by_city(city_id: int, db: Session = Depends(get_db)) -> schemas.TemperatureList:
    db_temperature = crud.get_temperature_by_city_id(db=db, city_id=city_id)

    if db_temperature is None:
        raise HTTPException(status_code=400, detail="Temperature not found")

    return db_temperature


@router.post("/temperatures/update/")
async def create_temperatures(db: Session = Depends(get_db)) -> None:
    cities = get_all_cities(db=db)
    local_parameters = parameters

    for city in cities:
        local_parameters["q"] = city.name
        response = requests.get(BASE_URL, params=local_parameters).json()

        crud.create_temperature(
            db=db,
            city_id=city.id,
            date_time=datetime.strptime(
                response["current"]["last_updated"], "%Y-%m-%d %H:%M"
            ),
            temperature=response["current"]["temp_c"],
        )
