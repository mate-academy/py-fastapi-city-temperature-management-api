from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud, models

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int | None = None
) -> list[models.DBTemperature]:
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.Temperature]
)
async def create_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[models.DBTemperature]:
    return await crud.create_temperatures_by_helper(db)
