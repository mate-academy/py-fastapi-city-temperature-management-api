from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio.session import AsyncSession

from dependecies import get_db
import crud.temperature as crud_temperature
import schemas


router = APIRouter()


@router.post("/temperatures/update/", response_model=schemas.TemperatureUpdate)
async def update_cities_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud_temperature.update_temperatures(db=db)


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
    city_id: int = Query(None)
):
    temperatures = await crud_temperature.get_all_temperatures(
        db=db,
        city_id=city_id
    )

    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail=f"No temperatures found for city with ID: {city_id}."
        )

    return temperatures
