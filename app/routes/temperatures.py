from typing import List

from fastapi import APIRouter, HTTPException

from crud import (
    get_all_cities,
    create_temperatures,
    get_all_temperatures,
    get_temperatures_by_city_id
)
from db.database import SessionDep
from schemas import (
    TemperatureRetrieveSchema,
    TemperatureListSchema
)

router = APIRouter()


@router.post("/temperatures/update/", response_model=List[TemperatureRetrieveSchema])
async def add_temperatures(db: SessionDep):
    db_cities = await get_all_cities(db=db)
    if not db_cities:
        raise HTTPException(status_code=404, detail="No cities in database")

    temperatures = await create_temperatures(db=db, cities=db_cities)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures fetched")

    return temperatures


@router.get("/temperatures/", response_model=List[TemperatureListSchema])
async def list_temperatures(db: SessionDep):
    temperatures = await get_all_temperatures(db=db)

    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures


@router.get("/temperatures/{city_id}", response_model=List[TemperatureListSchema])
async def retrieve_temperature(city_id: int, db: SessionDep):
    city_temperatures = await get_temperatures_by_city_id(db=db, city_id=city_id)

    if not city_temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")

    return city_temperatures
