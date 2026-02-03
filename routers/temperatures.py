from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import httpx
from ..database import SessionLocal
from .. import crud, schemas


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_city_coordinates(city_name: str) -> tuple[float, float]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    if not data.get("results"):
        raise ValueError(f"City '{city_name}' not found")

    city = data["results"][0]
    return city["latitude"], city["longitude"]


async def fetch_temperature(city_name: str) -> float:
    latitude, longitude = await get_city_coordinates(city_name)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    return data["current_weather"]["temperature"]


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    for city in cities:
        temp = await fetch_temperatures(city.name)
        crud.create_temperatures(db, city_id=city.id, temperature=temp)
    return {"message": "temperatures updated successfully"}


@router.get("", response_model=List[schemas.TemperatureRead])
def list_all(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
