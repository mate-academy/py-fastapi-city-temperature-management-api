from typing import Any, Coroutine
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from dependencies import get_db
from temperature import schemas, crud
from temperature.crud import update_all_temperatures_async
from temperature.models import Temperature

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: AsyncSession = Depends(get_db)) -> Coroutine[Any, Any, list[Temperature]]:
    temperatures = crud.get_all_temperatures(db=db)
    return temperatures


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_temperature(
        temperature: schemas.TemperatureCreate, db: AsyncSession = Depends(get_db)
) -> Coroutine[Any, Any, Temperature]:
    return crud.create_temperature(db=db, temperature=temperature)


@router.get("/temperatures/{city_id}/", response_model=schemas.Temperature)
async def read_temperature_by_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> Coroutine[Any, Any, Temperature | None]:
    db_temperature = crud.get_temperature_for_specific_city(db, city_id=city_id)
    if db_temperature is None:
        raise HTTPException(status_code=404, detail="City is not found")
    return db_temperature


@router.post("/temperatures/update")
async def update_temperatures(
        background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
) -> dict:
    await update_all_temperatures_async(db=db)
    background_tasks.add_task(update_all_temperatures_async, db)
    return {"message": "Temperature update initiated ..."}
