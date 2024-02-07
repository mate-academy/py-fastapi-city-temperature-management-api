from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.post("/temperatures/update")
async def temperatures_update(db: AsyncSession = Depends(get_db)):
    return await crud.fetch_temperatures(db)


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def temperatures_list(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperature(db=db)


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
async def temperatures_by_city_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature_by_id(db, city_id)
