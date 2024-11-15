import aiohttp
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database, schemas
from typing import List

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


async def fetch_temperature(city_name: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.open-meteo.com/v1/forecast?city={city_name}") as response:
            data = await response.json()
            return data["current"]["temperature"]


@router.post("/update")
async def update_temperatures(db: Session = Depends(database.SessionLocal)):
    cities = db.query(models.City).all()
    for city in cities:
        temperature = await fetch_temperature(city.name)
        temp_record = models.Temperature(
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=temperature
        )
        db.add(temp_record)
    db.commit()
    return {"message": "Temperatures updated"}


@router.get("/", response_model=List[schemas.Temperature])
def get_temperatures(db: Session = Depends(database.SessionLocal)):
    return db.query(models.Temperature).all()
