from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.temperature import crud, schemas

router = APIRouter()

@router.post("/temperatures/update", response_model=list[schemas.Temperature])
async def update_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperature(db=db)


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def get_temperature(
        city_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperature(db=db, city_id=city_id)
