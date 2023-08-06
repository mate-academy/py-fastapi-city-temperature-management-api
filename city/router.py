from datetime import datetime
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from city import schemas, crud
from dependecies import get_db
from settings import settings

router = APIRouter()

WEATHER_API = f"http://api.weatherstack.com/current?access_key={settings.WEATHER_API_KEY}"


@router.post("/cities/", response_model=schemas.CityCreate)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    weather_api = WEATHER_API + f"&query={city.name}"
    response = requests.get(weather_api).json()
    if "location" in response:
        return crud.create_city(db=db, city=city)
    raise HTTPException(
        status_code=404, detail="Check the city name. City doesn't exist"
    )


@router.get("/cities/", response_model=List[schemas.City])
def get_city_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def get_specific_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_specific_city(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)


@router.post("/temperatures/update/")
async def create_temperatures(db: Session = Depends(get_db)):
    cities = get_city_list(db=db)
    created_temperatures = []
    for city in cities:
        weather_api = WEATHER_API + f"&query={city.name}"

        response = await requests.get(weather_api).json()

        temperature = crud.create_temperature(
            db=db,
            city_id=city.id,
            date_time=datetime.strptime(
                response["location"]["localtime"], "%Y-%m-%d %H:%M"
            ),
            temperature=response["current"]["temperature"],
        )
        created_temperatures.append(temperature)
    return created_temperatures


@router.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperature_records(
    city_id: int = Query(None, alias="city_id"),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    if city_id:
        return crud.get_specific_city_temperature_record(db=db, city_id=city_id)

    return crud.get_temperature_records(db=db, skip=skip, limit=limit)
