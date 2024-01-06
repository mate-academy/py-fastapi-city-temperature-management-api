from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas
from temperature.models import DBTemperature

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int = None
) -> [DBTemperature]:
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=None)
async def update_all_city_temperature(
        db: AsyncSession = Depends(get_db)
) -> None:
    await crud.update_all_temperatures(db=db)
