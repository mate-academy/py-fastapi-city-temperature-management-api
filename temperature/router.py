from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def fetch_temperature_for_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperature_for_all_cities(db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperature_records(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    if city_id:
        return await crud.get_temperature_by_city_id(db, city_id)

    return await crud.get_all_temperature_records(db)
