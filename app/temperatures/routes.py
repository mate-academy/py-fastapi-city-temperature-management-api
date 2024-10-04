from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.cities.models import City
from app.temperatures.models import Temperature
from app.temperatures.schemas import TemperatureOut
from app.database import get_db
from datetime import datetime
import random

router = APIRouter()

@router.post("/temperatures/update", response_model=list[TemperatureOut])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    temperatures = []
    for city in cities:
        new_temperature = Temperature(
            city_id=city.id,
            temperature=random.uniform(10.0, 30.0),
            date_time=datetime.datetime.utcnow()
        )
        db.add(new_temperature)
        db.commit()
        db.refresh(new_temperature)
        temperatures.append(new_temperature)
    return temperatures

@router.get("/temperatures/", response_model=list[TemperatureOut])
def read_temperatures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    temperatures = db.query(Temperature).offset(skip).limit(limit).all()
    return temperatures

@router.get("/temperatures/{city_id}", response_model=list[TemperatureOut])
def read_city_temperatures(city_id: int, db: Session = Depends(get_db)):
    temperatures = db.query(Temperature).filter(Temperature.city_id == city_id).all()
    return temperatures
