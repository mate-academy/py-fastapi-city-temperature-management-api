from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud, schemas
from dependencies import get_db


router = APIRouter()


@router.post("/temperature/", response_model=schemas.Temperature)
async def create_temperature(
        temperature: schemas.TemperatureCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    return await crud.create_temperature(db=db, temperature=temperature)


@router.get("/temperature/", response_model=List[schemas.Temperature])
async def read_temperatures(db: AsyncSession = Depends(get_db)) -> List[schemas.Temperature]:
    temperatures = await crud.get_all_temperatures(db)
    return temperatures


@router.get("/temperature/{temperature_id}", response_model=schemas.Temperature)
async def read_temperature(temperature_id: int, db: AsyncSession = Depends(get_db)) -> schemas.Temperature:
    temperature = await crud.get_temperature(db, temperature_id)
    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperature
