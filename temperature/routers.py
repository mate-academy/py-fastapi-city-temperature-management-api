import time
from typing import Any, Sequence

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_city
from temperature import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.Temperature]
)
async def update_cities_temperature(
        db: AsyncSession = Depends(get_db)
):
    return await crud.update_temperatures(db=db)


@router.post("/temperatures/{city-id}/", response_model=schemas.Temperature)
async def update_citi_temperature(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_city = await get_city(city_id=city_id, db=db)
    async with httpx.AsyncClient() as client:
        return await crud.create_temperature(
            db_city=db_city, db=db, client=client
        )


@router.get("/temperatures/", response_model=list[schemas.Temperature])
@cache(expire=30)
async def read_temperatures(db: AsyncSession = Depends(get_db)
                            ) -> Sequence[Row | RowMapping | Any]:
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city-id}/", response_model=list[schemas.Temperature])
@cache(expire=30)
async def read_single_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> Sequence[Row | RowMapping | Any]:
    db_temperature = await crud.get_temperature(
        db=db,
        city_id=city_id
    )

    if db_temperature is None:
        raise HTTPException(
            status_code=400,
            detail="temperature not found"
        )

    return db_temperature
