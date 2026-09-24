import asyncio
from datetime import datetime, timezone
from typing import Annotated

import httpx
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import models, crud, schemas
from city import crud as city_crud
from temperature.weather import fetch_temperature


router = APIRouter()

@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_city_list(db)
    async with httpx.AsyncClient(timeout=10) as client:
        results = await asyncio.gather(
            *(fetch_temperature(client, city.name) for city in cities),
            return_exceptions=True,
        )
    now = datetime.now(timezone.utc)
    updated_records, deleted_records = [], []
    for city, result in zip(cities, results):
        if isinstance(result, (int, float)):
            updated_records.append(
                models.Temperature(
                    city_id=city.id,
                    date_time=now,
                    temperature=result,
                )
            )
        else:
            deleted_records.append(result)

    await crud.create_temperatures(db, updated_records)
    return {"updated_records": len(updated_records), "deleted_records": deleted_records}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_temperatures(db=db)

@router.get("/temperatures/", response_model=schemas.Temperature)
async def get_temperatures_by_city_id(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    if city_id is None:
        return await crud.get_all_temperatures(db)
    return await crud.get_temperature_by_city(db, city_id)
