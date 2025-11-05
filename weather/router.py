from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Temperature, City
from schemas import CityCreate, TemperatureUpdateResponse
from crud import (
    get_all_city_crud,
    create_city_crud,
    get_city_by_id_crud,
    update_city_crud,
    city_delete_crud,
    get_all_city_names_crud,
    update_temperature_cities_crud,
    get_all_temperaturs_crud,
    get_temparature_by_city_id_crud
)
from utils import get_temperature_for_cities

router = APIRouter()


@router.get("/cities", response_model=List[City], status_code=200)
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await get_all_city_crud(db)


@router.post("/cities", response_model=City, status_code=201)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_city_crud(db, city)


@router.get("/cities/{city_id}", response_model=City, status_code=200)
async def get_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city_by_id_crud(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.put("/cities/{city_id}", response_model=City, status_code=200)
async def update_city(
    city_id: int,
    city_data: CityCreate,
    db: AsyncSession = Depends(get_db)
):
    city = await update_city_crud(db, city_id, city_data)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await city_delete_crud(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")
    return


@router.post(
    "/temperatures/update",
    response_model=TemperatureUpdateResponse,
    status_code=201
)
async def update_temparatures_all_city(db: AsyncSession = Depends(get_db)):
    city_names = await get_all_city_names_crud(db)
    if not city_names:
        return {"updated": 0, "details": []}
    temperatures = await get_temperature_for_cities(city_names)
    updated_records = []
    for city, temp in temperatures:
        if city and temp is not None:
            record = await update_temperature_cities_crud(db, city, temp)
            if record:
                updated_records.append({"city": city, "temperature": temp})
    return {"updated": len(updated_records), "details": updated_records}


@router.get("/temperatures/", response_model=List[Temperature], status_code=200)
async def get_temperatures(
    city_id: Optional[int] = Query(None, description="ID of the city"),
    db: AsyncSession = Depends(get_db)
):
    if city_id is not None:
        temperature = await get_temparature_by_city_id_crud(db, city_id)
        if not temperature:
            raise HTTPException(
                status_code=404, detail=f"Temperature for city_id {city_id} not found."
            )
        return temperature
    else:
        temperatures = await get_all_temperaturs_crud(db)
        if not temperatures:
            raise HTTPException(status_code=404, detail="No temperatures found.")
        return temperatures
