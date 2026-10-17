from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database import get_db
import crud
import httpx

router = APIRouter(tags=["temperature"])
DBDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/temperatures", response_model=list[schemas.TemperatureResponse])
async def get_temperatures(db: DBDep):
    return await crud.get_temperatures(db)

@router.get("/temperatures/", response_model=list[schemas.TemperatureResponse])
async def get_temperature_by_city_id(city_id: int, db: DBDep):
    return await crud.get_temperature_by_city_id(db, city_id)

@router.post("/temperatures/update", response_model=list[schemas.TemperatureResponse], status_code=status.HTTP_200_OK)
async def update_temperatures(db: DBDep):
    try:
        return await crud.update_all_temperatures(db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch weather data",
        ) from exc
