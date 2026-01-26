from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperatures.crud import update_temperature
from temperatures import crud, schemas

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures_in_cities_endpoint(
        db: AsyncSession = Depends(get_db)
):
    await update_temperature(db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_all_temperatures_endpoint(
        city_id: int | None  = None, db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)
