import os
from datetime import datetime
from typing import List

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

load_dotenv()

router = APIRouter()
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {
                "key": WEATHER_API_KEY,
                "q": city.name
            }
            response = await client.get(BASE_URL, params=params)
            data = response.json()
            temperature_data = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=data['current']['temp_c']
            )
            crud.create_temperature(db=db, temperature=temperature_data)
    return {"message": "Temperatures updated"}


@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(skip: int = 0, limit: int = 10, db: Session = Depends(
    get_db
)):
    temperatures = crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures


@router.get("/{city_id}", response_model=List[schemas.Temperature])
def read_temperatures_by_city(city_id: str, db: Session = Depends(get_db)):
    temperatures = crud.get_temperatures_by_city(db, city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures
