from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas, database
from services import weather
from fastapi.concurrency import run_in_threadpool

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)

import asyncio


@router.post("/update")
async def update_temperatures(db: Session = Depends(database.get_db)):
    cities = await run_in_threadpool(crud.get_cities, db)
    if not cities:
        return {"message": "No cities found to update"}

    tasks = []
    for city in cities:
        tasks.append(weather.fetch_weather_for_city(city.name))

    results = await asyncio.gather(*tasks)

    updated_count = 0
    for city, temp in zip(cities, results):
        if temp is not None:
            temp_create = schemas.TemperatureCreate(
                city_id=city.id,
                temperature=temp
            )
            await run_in_threadpool(crud.create_temperature, db, temp_create)
            updated_count += 1

    return {"message": f"Updated temperatures for {updated_count} cities"}


@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(city_id: Optional[int] = None, skip: int = 0, limit: int = 100,
                      db: Session = Depends(database.get_db)):
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
