from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.exeptions import CityNotFound, TemperatureNotFound
from app.schemes.temperature import (
    TemperatureCreate, TemperatureUpdate, TemperatureResponse
)
from app.db.database import get_db, get_async_db
from app.db import crud

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperature"]
)


@router.get("/", response_model=list[TemperatureResponse])
def get_temperatures(
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)) -> list[TemperatureResponse]:
    if city_id is not None:
        return crud.get_temperature_by_city_id(db, city_id)
    return crud.get_all_temperatures(db, skip, limit)


@router.post("/", response_model=TemperatureResponse)
def create_temperature(
        data: TemperatureCreate,
        db: Session = Depends(get_db)) -> TemperatureResponse:
    try:
        return crud.create_temperature(db, data)
    except CityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/update/", response_model=list[TemperatureResponse])
async def update_temperature_all_cities(db: AsyncSession = Depends(get_async_db)) -> list[TemperatureResponse]:
    try:
        return await crud.auto_insert_temperature(db)
    except (CityNotFound, TemperatureNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{temperature_id}", response_model=TemperatureResponse)
def update_temperature(temperature_id: int, data: TemperatureUpdate, db: Session = Depends(get_db)) -> TemperatureResponse:
    try:
        return crud.update_temperature(db, temperature_id, data)
    except (CityNotFound, TemperatureNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{temperature_id}", status_code=204)
def delete_temperature(temperature_id: int, db: Session = Depends(get_db)) -> None:
    try:
        crud.delete_temperature(db, temperature_id)
    except TemperatureNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
