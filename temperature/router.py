from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud
from city import crud as city_crud
from temperature.service import fetch_temperature_by_coordinates

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"]
)


@router.get("/", response_model=list[schemas.TemperatureRead])
async def read_city_temperature(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 10
):
    if city_id is not None:
        db_city_temp = await crud.get_city_temperature_by_id(
            db=db,
            city_id=city_id,
            skip=skip,
            limit=limit
        )
    
        return db_city_temp
    
    return await crud.get_temperatures(
        db=db,
        skip=skip,
        limit=limit
    )


@router.post("/update", response_model=list[schemas.TemperatureRead], status_code=status.HTTP_201_CREATED)
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    cities = await city_crud.get_cities(db=db)
    temperatures = []
    for city in cities:
        latitude = city.additional_info["latitude"]
        longitude = city.additional_info["longitude"]

        temperature = await fetch_temperature_by_coordinates(latitude, longitude)
        if temperature is not None:
            created_record = await crud.create_temperature_record(
                db=db,
                temperature=schemas.TemperatureCreate(
                    city_id=city.id,
                    temperature=temperature
                )
            )
            temperatures.append(created_record)
    return temperatures
        