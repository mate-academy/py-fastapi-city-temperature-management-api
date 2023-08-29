import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city.crud import list_cities

from . import crud, schemas
from .service import temperature_for_specific_city

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(city_id: int|None = None, db: AsyncSession = Depends(get_db)):
    return await crud.list_temperatures(
        db=db,
    )


@router.post("/temperatures/update/")
async def update_temperature(
        db: AsyncSession = Depends(get_db)
):
    cities = await list_cities(db=db)
    await asyncio.gather(*[
        temperature_for_specific_city(city=city, db=db)
        for city in cities
    ])

    await db.commit()

    return {"message": "All temperatures are updated"}
