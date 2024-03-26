from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from crud.crude_temperatures import create_temperature, get_temperatures
from schemas.schemas import TemperatureCreate, Temperature
from services.temperature_service import fetch_temperature
from crud.crud_cities import get_cities

router = APIRouter()


@router.post("/temperatures/", response_model=Temperature)
async def create_temperature_record(temperature_data: TemperatureCreate, db: Session = Depends(get_db)):
    return create_temperature(db=db, temperature=temperature_data)


@router.get("/temperatures/", response_model=List[Temperature])
def read_temperatures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_temperatures(db, skip=skip, limit=limit)


@router.post("/temperatures/update")
async def update_temperatures(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    cities = get_cities(db)
    for city in cities:
        background_tasks.add_task(fetch_and_store_temperature, city.id, db)
    return {"message": "Temperature update started"}


async def fetch_and_store_temperature(city_id: int, db: Session):
    temperature = await fetch_temperature(city_id=city_id)
    temperature_data = TemperatureCreate(city_id=city_id, temperature=temperature)
    create_temperature(db=db, temperature=temperature_data)
