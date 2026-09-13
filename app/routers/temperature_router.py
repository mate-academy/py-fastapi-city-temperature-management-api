from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import temperature_schema
from app.services import temperature_service
from app.services import city_service

from dependencies import get_db

router = APIRouter(tags=["temperature"])

CommonDB = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/temperatures/update", response_model=list[temperature_schema.Temperature]
)
async def create_temperatures(db: CommonDB):
    return await temperature_service.create_temperatures(db)


@router.get(
    "/temperatures",
    response_model=list[temperature_schema.Temperature]
)
async def read_temperatures(db: CommonDB):
    return await temperature_service.get_all_temperatures(db=db)


@router.get(
    "/temperatures/{city_id}",
    response_model=list[temperature_schema.Temperature]
)
async def read_temperatures_by_city(city_id: int, db: CommonDB):
    db_city = await city_service.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await temperature_service.get_all_temperatures_by_city_id(
        db=db, city_id=city_id
    )
