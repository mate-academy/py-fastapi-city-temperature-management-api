from fastapi import APIRouter, Depends

from temperature import schemas
from temperature.dependencies.services import get_temperature_service
from temperature.services.temperature_service import TemperatureService

temperature_router = APIRouter()


@temperature_router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    service: TemperatureService = Depends(get_temperature_service),
):
    return await service.get_temperature_list()


@temperature_router.post("/temperatures/update/")
async def fetch_temperatures(
    service: TemperatureService = Depends(get_temperature_service),
):
    await service.update_cities_temperatures()
