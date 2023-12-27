from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureBase])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.temperatures(db=db)


@router.get(
    "/temperatures/{city_id}/", response_model=list[schemas.TemperatureBase]
)
async def get_temperatures_by_city_id(
        city_id: int, db: AsyncSession = Depends(get_db)
):
    return await crud.temperatures_by_city_id(db=db, city_id=city_id)


@router.post("/temperatures/", response_model=str)
async def update_cities_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.update_cities_temperature(db=db)
