from typing import List
from fastapi import APIRouter
from sqlalchemy import select

from src import models
from src.dependencies import DBSessionDep
from src.services import temperature_service
from src.schemas.temperature import TemperatureRead

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=list[TemperatureRead] | dict[str, str])
async def update_temperature_records_data(db: DBSessionDep):
    update_records = await temperature_service.update_temperature_records(db)
    if update_records:
        return update_records
    return {
        "message": "All temperature records are up-to-date",
    }


@router.get("/", response_model=List[TemperatureRead])
async def get_temperatures(db: DBSessionDep, city_id: int | None = None):
    stmt = select(models.Temperature)
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    result = await db.scalars(stmt)
    return result.all()
