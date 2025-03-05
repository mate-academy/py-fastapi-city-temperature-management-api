from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature_api import schemas, crud

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=List[schemas.Temperature])
async def read_all_temperatures_or_by_city_id(
    db: AsyncSession = Depends(get_db), city_id: int = None
):
    return await crud.get_temperatures(db=db, city_id=city_id)


@router.post("/update", response_model=dict)
async def update_temperature_for_cities(db: AsyncSession = Depends(get_db)):
    await crud.update_temperatures(db=db)

    return {"message": "Temperatures has been updated successfully"}
