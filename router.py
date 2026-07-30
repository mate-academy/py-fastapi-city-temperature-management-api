from typing import Annotated
import asyncio

from weather_service import get_city_temperature
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

import schemas, crud

router = APIRouter()

@router.get("/cities", response_model=list[schemas.City])
async def read_all_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)

@router.post("/cities", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_city(
        db=db,
        city=city
    )

@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_single_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city

@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_by_id(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    new_data: schemas.CityCreate,
):
    db_city = await crud.update_city(db=db, city_id=city_id, new_data=new_data)
    existing = await crud.get_city_by_name(db=db, name=new_data.name)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    if existing and existing.id != city_id:
        raise HTTPException(status_code=400, detail="City already exist")

    return db_city

@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_single_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.delete_city(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city

@router.get("/temperatures", response_model=list[schemas.Temperature])
async def read_all_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = None,
):
    return await crud.get_temperature_list(db=db, city_id=city_id)

@router.post("/temperatures/update")
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    cities = await crud.get_all_cities(db)
    if not cities:
        raise HTTPException(status_code=404, detail="City not found")
    
    tasks = [
    get_city_temperature(city.name)
    for city in cities
]
    temperatures = await asyncio.gather(
        *tasks,
        return_exceptions=True,
)
    updated = 0
    for city, temp in zip(cities, temperatures):
        print(city.name, temp)
        if isinstance(temp, Exception):
            continue
        await crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=temp, # type: ignore
    )
        updated += 1
    return {"updated": updated}