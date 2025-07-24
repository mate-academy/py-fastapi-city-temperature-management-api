from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import temperature as schemas
from app.crud import temperature as crud
from app.models import city as models
from app.db import SessionLocal
from app.utils import fetch_temperature_async
import asyncio
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/temperatures", response_model=list[schemas.Temperature])
def list_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    if city_id:
        return crud.get_temperatures_for_city(db, city_id)
    return crud.get_all_temperatures(db)

@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    results = await asyncio.gather(*(fetch_temperature_async(city.name) for city in cities))

    for city, temp in zip(cities, results):
        if temp is not None:
            await asyncio.to_thread(
                crud.create_temperature,
                db,
                schemas.TemperatureCreate(city_id=city.id, temperature=temp)
            )

    return {"message": "Temperatures updated."}

