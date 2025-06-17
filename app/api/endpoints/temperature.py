from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.crud.temperature import (
    get_all_temperatures,
    get_temperature_with_city_id,
    fetch_and_store_temperatures as crud_fetch_and_store_temperatures,
)
from app.schemas.temperature import TemperatureReadSchema
from app.schemas.city import MessageResponse


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


@router.get(
    "/",
    response_model=List[TemperatureReadSchema],
    summary="Get all temperature records"
)
async def get_all_temperature_records(db: AsyncSession = Depends(get_db)):
    return await get_all_temperatures(db)


@router.get(
    "/{city_id}",
    response_model=List[TemperatureReadSchema],
    summary="Get temperature records for a specific city"
)
async def get_temperature_records_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):

    return await get_temperature_with_city_id(db, city_id)


@router.post(
    "/update",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch and store current temperatures for all cities"
)
async def update_temperatures_endpoint(db: AsyncSession = Depends(get_db)):

    return await crud_fetch_and_store_temperatures(db)