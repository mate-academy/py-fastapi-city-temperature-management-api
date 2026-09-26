from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud as city_crud

from dependencies import get_session
from temperature import crud
from temperature.schemas import TemperatureRead
from temperature.utils import fetch_temperature

router = APIRouter(prefix="/temperatures",
                   tags=["temperatures"])

@router.get("", response_model=list[TemperatureRead])
async def get_temperatures(
        city_id: int | None = Query(None,
                                    description="Filter by city id"),
        session: AsyncSession = Depends(get_session)
):
    return await crud.get_temperatures(session, city_id)

@router.post(
    "/update",
    response_model=list[TemperatureRead],
    status_code=status.HTTP_201_CREATED,
)
async def update_temperatures(session: AsyncSession = Depends(get_session)):
    cities = await city_crud.get_cities(session)
    saved = []
    for city in cities:
        value = await fetch_temperature(city.name)
        record = await crud.save_temperature(session, city.id, value)
        saved.append(record)
    return saved