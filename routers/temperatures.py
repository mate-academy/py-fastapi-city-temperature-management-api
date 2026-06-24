import asyncio
from typing import Optional

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud, schemas
from dependencies import get_db
from weather_service import WeatherFetchError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db, limit=10_000)

    updated_cities: list[str] = []
    failed_cities: list[str] = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_current_temperature(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for city, result in zip(cities, results):
        if isinstance(result, WeatherFetchError) or isinstance(result, Exception):
            failed_cities.append(city.name)
            continue
        temperature, date_time = result
        crud.create_temperature_record(
            db, city_id=city.id, temperature=temperature, date_time=date_time
        )
        updated_cities.append(city.name)

    return schemas.TemperatureUpdateResult(
        updated_cities=updated_cities, failed_cities=failed_cities
    )


@router.get("", response_model=list[schemas.TemperatureResponse])
def read_temperatures(
    city_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
