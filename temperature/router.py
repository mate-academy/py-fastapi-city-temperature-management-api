from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud, schemas
from city import crud as city_crud
from dependencies import get_db

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/", response_model=schemas.Temperature, status_code=201)
async def create_temperature(
    temperature: schemas.TemperatureCreate, db: AsyncSession = Depends(get_db)
):
    # Перевіряємо, чи існує місто
    city = await city_crud.get_city(db, city_id=temperature.city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.create_temperature(db=db, temperature=temperature)


@router.get("/", response_model=List[schemas.Temperature])
async def read_temperatures(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    temperatures = await crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures


@router.get("/{temperature_id}", response_model=schemas.Temperature)
async def read_temperature(
    temperature_id: int, db: AsyncSession = Depends(get_db)
):
    db_temperature = await crud.get_temperature(
        db, temperature_id=temperature_id
    )
    if db_temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return db_temperature


@router.get(
    "/city/{city_id}", response_model=List[schemas.TemperatureWithCity]
)
async def read_temperatures_by_city(
    city_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    # Перевіряємо, чи існує місто
    city = await city_crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    temperatures = await crud.get_temperatures_by_city(
        db, city_id=city_id, skip=skip, limit=limit
    )
    return temperatures


@router.get("/city/{city_id}/latest", response_model=schemas.Temperature)
async def read_latest_temperature_by_city(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    # Перевіряємо, чи існує місто
    city = await city_crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    temperature = await crud.get_latest_temperature_by_city(
        db, city_id=city_id
    )
    if not temperature:
        raise HTTPException(
            status_code=404, detail="No temperature data found for this city"
        )

    return temperature
