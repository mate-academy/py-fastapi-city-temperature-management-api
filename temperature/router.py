from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
    city_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(city_id=city_id, db=db)


@router.post("/temperatures/update/", response_model=dict)
async def update_temperature(db: AsyncSession = Depends(get_db)):
    await crud.get_and_store_temperatures(db)
    return {"message": "Temperature data updated"}
