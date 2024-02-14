from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature_app import crud, schemas
from temperature_app.weather import get_current_temperature

router = APIRouter()


@router.post(
    "/temperatures/update/",
    response_model=dict,
    status_code=200
)
async def update_temperatures(
        db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    data = await get_current_temperature(db)

    return await crud.create_update_temperature(db, data)


@router.get(
    "/temperatures/",
    response_model=List[schemas.Temperature],
    status_code=200
)
async def read_temperatures(
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    return await crud.get_all_temperatures(db)


@router.get(
    "/temperatures/{city_id}/",
    status_code=200
)
async def read_temperatures_for_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    temperature = await crud.get_temperatures_for_city(db, city_id)
    if temperature is None:
        raise HTTPException(
            status_code=404,
            detail=f"Temperature info for city with id: {city_id} not found"
        )
    return temperature
