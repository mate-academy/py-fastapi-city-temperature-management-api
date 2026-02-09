import asyncio
from typing import Annotated, Sequence

import httpx

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import get_cities
from dependencies import get_session

from temperatures import crud, models, schemas, service


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/temperatures/update",
    response_model=list[schemas.Temperature],
    tags=["temperatures"],
    summary="Update temperatures"
)
async def create_temperatures(
        db: SessionDep
):
    cities = await get_cities(db=db)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    async with httpx.AsyncClient() as client:
        tasks = [service.fetch_weather(client, city) for city in cities]
        temperatures = await asyncio.gather(*tasks)

    new_temperatures = []
    for data in temperatures:
        if data:
            temp = models.Temperature(**data)
            new_temperatures.append(temp)

    if new_temperatures:
        db.add_all(new_temperatures)
        await db.commit()

    return new_temperatures


@router.get(
    "/temperatures",
    response_model=Sequence[schemas.Temperature],
    tags=["temperatures"],
    summary="Get all temperatures or specific temperature"
)
async def get_temperatures_or_city_temperature(
        db: SessionDep,
        city_id: int | None = None
):
    if city_id:
        return await crud.get_temperatures_by_city_id(db=db, city_id=city_id)
    return await crud.get_temperatures(db=db)
