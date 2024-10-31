from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from dependencies import get_db
from temperatures.schemas import TemperatureResponse
from temperatures.crud import (
    get_temperatures,
    fetch_and_store_temperatures,
    get_all_cities
)


router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db)
    await fetch_and_store_temperatures(db, cities)
    return {"message": "Temperature data updated"}


@router.get("/temperatures/", response_model=List[TemperatureResponse])
async def read_temperatures(
    city_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    temperatures = await get_temperatures(db, city_id)
    return temperatures
