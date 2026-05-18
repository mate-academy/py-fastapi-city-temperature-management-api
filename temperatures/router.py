import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from temperatures import crud, service
from temperatures.schemas import TemperatureRead
from cities import crud as cities_crud


router = APIRouter()

@router.get("/temperatures", response_model=List[TemperatureRead])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature(db=db)

@router.get("/temperatures/{city_id}", response_model=List[TemperatureRead])
async def get_temperature(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature(db=db, city_id=city_id)

@router.post("/temperatures/update", response_model=List[TemperatureRead])
async def update_temperature(db: AsyncSession = Depends(get_db)):
    cities = await cities_crud.get_cities(db)

    results = []
    for city in cities:
        temp = await service.fetch_temperature(city.name)

        if temp is None:
            continue

        record = await crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=temp,
            date_time=datetime.datetime.now(),
        )
        results.append(record)

    return results
