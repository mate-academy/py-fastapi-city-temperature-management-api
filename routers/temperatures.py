from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from starlette.concurrency import run_in_threadpool

from dependencies import get_db
import models
import schemas
import crud
import httpx
import asyncio
import os

from httpx import RequestError, HTTPStatusError

from dotenv import load_dotenv
load_dotenv()


router = APIRouter(prefix="/temperatures", tags=["temperatures"])

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise RuntimeError("WEATHER_API_KEY is not not set. Please add it to your .env file")


async def fetch_temperature_for_city(city_name: str) -> Optional[float]:
    async with httpx.AsyncClient() as client:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
            f"&appid={WEATHER_API_KEY}&units=metric"
        )
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data["main"]["temp"]
        except (RequestError, HTTPStatusError, KeyError):
            return None


@router.post("/update/", response_model=List[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = await run_in_threadpool(lambda: db.query(models.City).all())

    tasks = [fetch_temperature_for_city(str(city.name)) for city in cities]
    temps = await asyncio.gather(*tasks)

    created_records = []

    for city, temp in zip(cities, temps):
        if temp is not None:
            record = schemas.TemperatureCreate(city_id=city.id, temperature=temp)
            created = await run_in_threadpool(crud.create_temperature, db, record)
            created_records.append(created)

    return created_records


@router.get("/", response_model=List[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    if city_id:
        return crud.get_temperatures_by_city(db, city_id)
    return crud.get_all_temperatures(db)
