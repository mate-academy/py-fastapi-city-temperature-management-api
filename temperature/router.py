from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()


@router.post("/temperatures/update/", status_code=201)
async def update_all_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    return await crud.update_all_temperatures(db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db, city_id=city_id)
