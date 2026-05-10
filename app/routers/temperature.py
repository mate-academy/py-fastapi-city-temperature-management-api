from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_database
from app.temperature.models import Temperature
from app.temperature import schemas
from app.temperature import crud


router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.TemperatureList])
async def read_temperatures(
	db: AsyncSession = Depends(get_database)
) -> list[Temperature]:
	return await crud.get_temperature_list(db)


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def read_temperatures_by_city_id(
    city_id: int,
	db: AsyncSession = Depends(get_database)
) -> list[Temperature]:
	return await crud.get_temperature_list_by_city_id(db, city_id)


@router.post("/temperatures/update")
async def refresh_temperatures(
	db: AsyncSession = Depends(get_database)
) -> None:
	return await crud.update_temperatures(db)
