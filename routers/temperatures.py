from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from session_db import db_session
import crud.temperatures
import crud.cities
import schemas.temperature
import python_weather

router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.temperature.GetTemperature])
def get_temperature_all(city_id: int | None = None, db: Session = Depends(db_session)):
    return crud.temperatures.get_temperature(db, city_id)


@router.get("/temperatures/{city_id}", response_model=schemas.temperature.GetTemperature)
def get_temperature_by_id(city_id: int, db: Session = Depends(db_session)):
    db_city_id = crud.temperatures.get_temperature_id(db, city_id)
    if db_city_id is None:
        raise HTTPException(
            status_code=404,
            detail= f"Temperature record not found for city ID {city_id}"
        )
    return db_city_id


@router.post("/temperatures", response_model=schemas.temperature.GetTemperature)
async def create_temp(create_t: schemas.temperature.CreateTemperature, db: Session = Depends(db_session)):
    city_name = crud.temperatures.get_name_city_by_id(db, city_id=create_t.city_id)
    if city_name is None:
        raise HTTPException(
            status_code=404,
            detail=f"City with ID {create_t.city_id} not found."
        )
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city_name)
    db_create_temp = crud.temperatures.create_temperature(db=db, create_temp=create_t, today_weather=weather.temperature)
    if db_create_temp is None:
        raise HTTPException(
            status_code=400,
            detail= "Temperature exists!"
        )
    return db_create_temp


@router.post("/temperatures/update", response_model=list[schemas.temperature.GetTemperature])
async def update_temp(db: Session = Depends(db_session)):
    cities = crud.cities.get_all_cities(db)
    if not cities:
        raise HTTPException(
            status_code= 404,
            detail= "Not cities"
        )
    result = []
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        for city in cities:
            weather = await client.get(city.name)
            db_update = crud.temperatures.update_temperature(db, city, weather.temperature)
            result.append(db_update)

    return result

