import asyncio
from collections.abc import Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.crud import get_cities
from app.services.city_weather_service import TemperatureService
from app.temperature import crud, models, schemas
from core import get_db

temperature_router = APIRouter(prefix="/temperatures", tags=["Temperature"])


@temperature_router.get("/", response_model=list[schemas.Temperature])
async def list_temperatures(
    city_id: int = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Sequence[models.Temperature]:
    """Retrieves a list of temperature records, optionally filtered by city ID."""
    return await crud.get_temperatures(db, city_id, skip, limit)


@temperature_router.post(
    "/update/",
    response_model=list[schemas.Temperature],
    status_code=status.HTTP_201_CREATED,
)
async def update_cities_temperatures(
    skip: int = 0,
    limit: int = 100,
    temp_service: TemperatureService = Depends(),
    db: AsyncSession = Depends(get_db),
) -> list[models.Temperature]:
    """Fetches and updates temperature data for all registered cities."""
    cities = await get_cities(db, skip=skip, limit=limit)

    api_tasks = [temp_service.get_city_temperature_data(city) for city in cities]
    weather_data_list = await asyncio.gather(*api_tasks)

    updated_temps = []
    for data in weather_data_list:
        if data:
            new_temp = await crud.update_city_temperature(db=db, temperature_data=data)
            if new_temp:
                updated_temps.append(new_temp)

    return updated_temps
