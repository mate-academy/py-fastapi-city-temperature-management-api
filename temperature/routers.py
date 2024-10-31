from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import services, schemas, crud

router = APIRouter()

@router.post("/temperatures/update/", status_code=200)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await services.update_temperature(db)
    if result:
        return {"message": "Temperatures have been updated successfully"}


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def read_temperatures(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db, city_id=city_id)
