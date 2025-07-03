from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, crud, schemas, weather, models
import asyncio


router = APIRouter(tags=["temperatures"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Temperature])
def list(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)

@router.post("/update")
async def update_temperatures():
    db = database.SessionLocal()
    try:
        cities = crud.get_cities(db)
    finally:
        db.close()

    async def process_city(city):
        temp = await weather.get_weather_data(city.name)
        db_local = database.SessionLocal()
        try:
            return crud.create_temperature(db_local, schemas.TemperatureCreate(
                city_id=city.id,
                temperature=temp
            ))
        finally:
            db_local.close()

    results = await asyncio.gather(*[process_city(city) for city in cities])
    return results