from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud, schemas
from dependencies import get_db


router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.TemperatureSerializer]
)
async def cities_temperature_list(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_temperatures(db=db, skip=skip, limit=limit)


@router.get(
    "/temperatures/{city_id}/",
    response_model=schemas.TemperatureSerializer
)
async def city_temperature_detail(
        city_id: int, db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperature_by_city_id(db, city_id=city_id)


@router.post("/temperatures/update/")
async def update_temperature_for_all_cities(
        db: AsyncSession = Depends(get_db)
) -> dict:
    await crud.update_temperatures(db=db)
    return {"temperatures": "update"}
