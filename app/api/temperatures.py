from fastapi import APIRouter, Depends
from app.schemas.temperature import TemperatureResponse
from app.api.dependencies import get_temperature_service
from app.services.temperature_service import TemperatureService

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=list[TemperatureResponse])
async def get_all_temperatures(
        city_id: int | None = None,
        service: TemperatureService = Depends(get_temperature_service)):
    if city_id:
        return await service.get_history_by_city(city_id)
    return await service.get_all_history()


@router.post("/update")
async def update_temperatures(
        service: TemperatureService =
        Depends(get_temperature_service)):
    await service.update_all_cities_weather()
    return {"message": "Temperatures updated successfully"}
