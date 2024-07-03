from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    await crud.update_all_temperatures(db)
    return {"message": "Temperatures updated"}


@router.get("/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.Temperature]:
    temperatures = await crud.get_all_temperatures(db=db)
    return temperatures


@router.get(
    "/{city_id}/", response_model=list[schemas.Temperature]
)
async def read_temperatures_for_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    temperatures = await crud.get_temperatures_by_city(db=db, city_id=city_id)
    return temperatures
