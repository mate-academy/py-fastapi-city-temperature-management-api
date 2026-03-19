from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("", response_model=list[schemas.TemperatureOut])
async def read_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_temperatures(db=db, city_id=city_id)


@router.post("/update", response_model=schemas.TemperatureOut)
async def update_temperature(
    temperature: schemas.TemperatureCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_temperature(db=db, temperature=temperature)