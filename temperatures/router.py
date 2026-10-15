from fastapi import APIRouter

from dependencies import DbSession
from temperatures import schemas, crud
from temperatures.services import update_temperatures

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update/", response_model=schemas.TemperatureUpdateResult)
async def update_temperature_in_all_cities_in_db(db: DbSession):
    return await update_temperatures(db=db)


@router.get("", response_model=list[schemas.TemperatureSchema])
async def temperature_list(db: DbSession, city_id: int | None = None):
    return await crud.get_temperatures(db=db, city_id=city_id)
