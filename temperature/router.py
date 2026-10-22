from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()

@router.get("/temperatures", response_model=list[schemas.Temperature])
async def get_temps_list_by_city_id(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    if city_id:
        return await crud.get_temperatures_by_city_id(city_id=city_id, db=db)
    return await crud.get_all_temperatures(db=db)

@router.post("/temperatures/update")
async def update_temperature( db: AsyncSession = Depends(get_db)):
    return await crud.fetch_and_store_temperatures(db=db)