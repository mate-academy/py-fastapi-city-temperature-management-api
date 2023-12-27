from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureBase])
async def get_all_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.all_temperature(db=db)


@router.get("/temperatures/{city_id}/", response_model=list[schemas.TemperatureBase])
async def get_all_temperature_by_city_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.all_temperature_by_city_id(db=db, city_id=city_id)


@router.post("/temperatures/", response_model=str)
async def update_all_city_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.update_all_city_temperature(db=db)
