from datetime import datetime
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from city import schemas, crud
from dependencies import get_db
from settings import settings

router = APIRouter()
WEATHER_API = f"https://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}"


@router.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)) -> schemas.City:
    weather_api = WEATHER_API + f"&q={city.name}&aqi=no"
    response = requests.get(weather_api).json()
    if "location" in response:
        return crud.create_city(db=db, city=city)
    raise HTTPException(
        status_code=404, detail="Please check the city name. City doesn't exist."
    )


@router.get("/cities", response_model=List[schemas.CityBase])
def read_cities(
        db: Session = Depends(get_db),
        skip: int = Query(0, description="Skip N items", ge=0),
        limit: int = Query(100, description="Limit the number of items to retrieve", le=100)
) -> List[schemas.CityBase]:
    return crud.get_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> schemas.City:
    db_city = read_city(city_id=city_id, db=db)
    return crud.update_city(db=db, db_city=db_city, city=city)


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)) -> str:
    db_city = read_city(city_id=city_id, db=db)
    return crud.delete_city(db=db, db_city=db_city)


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


@router.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperature_records(
        city_id: int = Query(None, alias="city_id"),
        db: Session = Depends(get_db),
        skip: int = Query(0, description="Skip N items", ge=0),
        limit: int = Query(100, description="Limit the number of items to retrieve", le=100)
) -> List[schemas.Temperature]:
    if city_id:
        return crud.get_specific_city_temperature_records(db=db, city_id=city_id)
    return crud.get_temperature_records(db=db, skip=skip, limit=limit)
