from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud

router = APIRouter()


@router.post("/temperatures/update/")
async def get_temperature_updates(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures_in_cities(db=db)


@router.get("/temperatures/")
async def get_temperature_records(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None
):
    return await crud.get_temperature_records(db=db, city_id=city_id)
