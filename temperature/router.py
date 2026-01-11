import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, crud
from dependencies import get_db

from city import crud as crud_city
from weather_client import fetch_current_temp

router = APIRouter()

@router.get("/temperatures/?city_id={city_id}/", response_model=list[schemas.Temperature])
async def read_temperatures(db: Annotated[AsyncSession, Depends(get_db)], city_id: int | None = None):
    if city_id is None:
        return await crud.get_all_temperature_records(db=db)

    return await crud.get_temperature_by_city_id(db=db, city_id=city_id)

@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    cities = await crud_city.get_all_cities(db=db)

    tasks = [fetch_current_temp(city.name) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    created_rows: list = []

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            print(f"[fetch error] {city.name}: {repr(result)}")
            continue

        row = await crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=float(result),
        )
        created_rows.append(row)

    await db.commit()
    return created_rows