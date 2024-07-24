import asyncio
from datetime import datetime
from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from temperature import crud, schemas
from db.database import get_db
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
API_KEY = os.getenv("WEATHER_API_KEY")


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http: //api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}"
            )
            response.raise_for_status()
            data = response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Failed to fetch temperature"
            )


@router.post(
    "/temperatures/update/", response_model=List[schemas.Temperature]
)
async def update_temperatures(db: Session = Depends(get_db)) -> List[schemas.Temperature]:
    cities = crud.get_cities(db)
    temperatures = []

    async def fetch_and_store(city) -> schemas.Temperature:
        temperature = await fetch_temperature(city.name)
        db_temperature = schemas.TemperatureCreate(
            city_id=city.id, date_time=datetime.now(), temperature=temperature
        )
        return crud.create_temperature(db, db_temperature)

    tasks = [fetch_and_store(city) for city in cities]
    temperatures = await asyncio.gather(*tasks)
    return temperatures


@router.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperatures(
    skip: int = 0,
    limit: int = 10,
    city_id: int = None,
    db: Session = Depends(get_db),
) -> List[schemas.Temperature]:
    if city_id:
        temperatures = crud.get_temperature_by_city(
            db, city_id=city_id, skip=skip, limit=limit
        )
    else:
        temperatures = crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures
