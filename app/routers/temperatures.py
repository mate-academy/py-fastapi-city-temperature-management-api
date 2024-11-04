from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud import temperature as temperature_crud, city as city_crud
from app.schemas.temperature import Temperature, TemperatureCreate
from app.utils.temperature_api import fetch_current_temperature

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/update", response_model=List[Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in the database.")

    temperature_records = []
    for city in cities:
        temperature = await fetch_current_temperature(city.name)
        temperature_create = TemperatureCreate(city_id=city.id, temperature=temperature)
        temperature_record = temperature_crud.create_temperature(db, temperature_create)
        temperature_records.append(temperature_record)

    return temperature_records

@router.get("/", response_model=List[Temperature])
def get_all_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    temperatures = temperature_crud.get_temperature(db, city_id=city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found.")
    return temperatures
