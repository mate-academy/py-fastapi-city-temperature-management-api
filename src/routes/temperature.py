from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.temperature import TemperatureService
from src.database.sqlite_db import get_sqlite_db
from src.models import TemperatureModel
from src.schemas.temperature import MessageResponseSchema, TemperatureResponseSchema

router = APIRouter()


def get_temperature_service(db: AsyncSession = Depends(get_sqlite_db)) -> TemperatureService:
    return TemperatureService(db)


@router.post("/temperatures/update")
async def fetch_temperature(
    temperature_service: TemperatureService = Depends(get_temperature_service)
) -> MessageResponseSchema:
    await temperature_service.update_all_cities_temperatures()
    return MessageResponseSchema(message="Temperatures updated successfully")


@router.get("/temperatures", response_model=list[TemperatureResponseSchema])
async def get_temperature(
    temperature_service: TemperatureService = Depends(get_temperature_service)
) -> list[TemperatureModel]:
    return await temperature_service.get_temperature()


@router.get("/temperatures/{city_id}", response_model=TemperatureResponseSchema)
async def get_temperature_by_city_id(
    city_id: int,
    temperature_service: TemperatureService = Depends(get_temperature_service)
) -> TemperatureResponseSchema | None:
    return await temperature_service.get_temperature_by_city_id(city_id)
