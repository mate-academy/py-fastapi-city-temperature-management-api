from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from city_api.models import City
from temperature_api.schemas import Temperature, TemperatureCreate
from temperature_api.models import Temperature as TemperatureModel
from dependencies import get_db
from temperature_api.weather import get_current_temperature

temp_router = APIRouter()


@temp_router.post("/temperatures/update/", response_model=Temperature)
async def update_temperatures(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    cities = db.query(City).all()
    for city in cities:
        temperature = await get_current_temperature(city.name)
        temperature_data = TemperatureCreate(
            city_id=city.id, date_time=datetime.utcnow(),
            temperature=temperature
        )
        db_temperature = TemperatureModel(**temperature_data.model_dump())
        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)
    return {"message": "Temperature records updated successfully."}


@temp_router.get("/temperatures/", response_model=list[Temperature])
def get_temperatures(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    temperatures = db.query(TemperatureModel).offset(skip).limit(limit).all()
    return temperatures


@temp_router.get("/temperatures/", response_model=list[Temperature])
def get_temperature_by_city(
    city_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    temperatures = db.query(TemperatureModel).filter(
        TemperatureModel.city_id == city_id
    ).offset(skip).limit(limit).all()
    return temperatures
