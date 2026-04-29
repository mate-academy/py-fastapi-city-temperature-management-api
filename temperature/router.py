from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_http_client
from temperature import schemas
from temperature.crud import get_temperature
from temperature.weather_service import update_all_temperatures

router = APIRouter()


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.Temperature],
)
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
):
    try:
        return await update_all_temperatures(db=db, client=client)
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Weather service is currently unavailable",
        )


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = None,
):
    return await get_temperature(db=db, city_id=city_id)
