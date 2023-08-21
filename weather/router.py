from datetime import datetime

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from settings import settings
from weather import schemas, crud

router = APIRouter()
WEATHER_API = (
    f"https://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}"
)


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate, db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="This city already exists")

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)) -> list[schemas.City]:
    return crud.get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=400, detail="City not found")

    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)
) -> schemas.City:
    db_city = read_single_city(db=db, city_id=city_id)

    return crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)) -> dict:
    db_city = read_single_city(db=db, city_id=city_id)

    crud.delete_city(db=db, city_id=city_id)
    return {"message": f"{db_city.name} deleted successfully."}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(db: Session = Depends(get_db)) -> list[schemas.Temperature]:
    return crud.get_all_temperatures(db)


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
def read_temperature_by_city(
    city_id: int, db: Session = Depends(get_db)
) -> schemas.Temperature:
    db_temperature = crud.get_temperature_by_city_id(db=db, city_id=city_id)

    if db_temperature is None:
        raise HTTPException(status_code=400, detail="Temperature not found")

    return db_temperature


@router.post("/temperatures/update")
async def create_temperatures(db: Session = Depends(get_db)) -> None:
    cities = read_cities(db=db)
    for city in cities:
        weather_api = WEATHER_API + f"&q={city.name}&aqi=no"

        response = requests.get(weather_api).json()

        crud.create_temperature(
            db=db,
            city_id=city.id,
            date_time=datetime.strptime(
                response["current"]["last_updated"], "%Y-%m-%d %H:%M"
            ),
            temperature=response["current"]["temp_c"],
        )
