import asyncio
from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from app import schemas, crud, models
from app.weather import get_temperature_from_api


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_city_list(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.CityList)
async def read_single_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return db_city


@router.post("/cities/", response_model=schemas.CityList)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="This city is already exists"
        )
    return await crud.create_city(
        db=db, city=city
    )


@router.patch("/cities/{city_id}/", response_model=schemas.CityList)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    db_city.name = city_update.name
    if city_update.additional_info is not None:
        db_city.additional_info = city_update.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    await db.delete(db_city)
    await db.commit()


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def read_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: Optional[int] = None
):
    if city_id is not None:
        return await crud.get_temperatures_by_city_id(
            db=db, city_id=city_id
        )
    return await crud.get_temperature_list(
        db=db
    )


@router.post("/temperatures/update/", response_model=list[schemas.TemperatureList])
async def create_temperature_for_all_cities(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    cities = await crud.get_city_list(db=db)
    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities found in database"
        )
    task = [get_temperature_from_api(city.name) for city in cities]
    temperatures = await asyncio.gather(*task)
    new_records = []
    for city, temp in zip(cities, temperatures):
        db_temperatures = models.DBTemperature(
            city_id=city.id,
            temperature=temp,
            date_time=datetime.now()
        )
        db.add(db_temperatures)
        new_records.append(db_temperatures)
    await db.commit()
    for record in new_records:
        await db.refresh(record)
    return new_records
