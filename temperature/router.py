import asyncio

import httpx
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud, schemas, models
from cities.models import City
from dependencies import get_db
from temperature.utils import fetch_temperature_for_city


router = APIRouter()


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperature_records(db: AsyncSession = Depends(get_db)):
    stmt = select(City)
    cities = await db.scalars(stmt)
    async with httpx.AsyncClient() as client:
        tasks = [fetch_temperature_for_city(city, client) for city in cities]
        records = []
        for coro in asyncio.as_completed(tasks):
            record = await coro
            if record:
                records.append(record)
    temperatures = await db.scalars(
        insert(models.Temperature)
        .values(records)
        .returning(models.Temperature),
    )
    await db.commit()
    return temperatures


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    return await crud.read_temperatures(
        city_id=city_id, skip=skip, limit=limit, db=db
    )
