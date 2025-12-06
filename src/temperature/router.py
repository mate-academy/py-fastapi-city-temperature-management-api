from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(db: AsyncSession = Depends(get_db), city_id: int | None = None):
    return await crud.get_all_temperatures(db=db, city_id=city_id)

@router.post("/temperatures/update/", response_model=schemas.TemperatureUpdate)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_all_temperatures(db=db)

