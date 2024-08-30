import asyncio
from typing import Sequence

import httpx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from city_temperature_app import (
    crud,
    models,
    schemas,
)
from city_temperature_app.get_temperature_from_api import (
    fetch_temperatures_from_api
)
from database import SessionLocal, get_db


router = APIRouter()


def get_temperatures_or_404(
        temperatures: Sequence[models.Temperature],
        detail: str
) -> Sequence[models.Temperature]:
    if not temperatures:
        raise HTTPException(
            status_code=404, detail=detail
        )
    return temperatures


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db)
) -> Sequence[models.Temperature]:
    temperatures = await crud.get_temperatures(db)
    return get_temperatures_or_404(
        temperatures, "There are no temperatures yet"
    )


@router.get(
    "/temperatures/{city_id}",
    response_model=list[schemas.Temperature]
)
async def read_temperature_by_city_id(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> Sequence[models.Temperature]:
    temperatures = await crud.get_temperatures(db, city_id)
    return get_temperatures_or_404(
        temperatures,
        f"There are no temperatures yet for city with id {city_id}"
    )


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    cities = await crud.get_cities(db)

    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_temperatures_from_api(client, city, SessionLocal)
            for city in cities
        ]
        await asyncio.gather(*tasks)

    return {"status": "Temperatures updated"}
