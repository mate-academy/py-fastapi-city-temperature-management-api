import asyncio
import httpx

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import City, Temperature
from app.dependencies.database import get_db
from app.schemas.temperature import TemperatureRead
from app.services.weather import get_current_temperature


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.get(
    "",
    response_model=list[TemperatureRead],
)
async def get_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[Temperature]:
    query = select(Temperature)

    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)

    return result.scalars().all()


async def fetch_temperature_for_city(
    city: City,
    client: httpx.AsyncClient,
) -> Temperature:
    date_time, temperature = await get_current_temperature(
        client,
        city.name,
    )

    return Temperature(
        city_id=city.id,
        date_time=date_time,
        temperature=temperature,
    )


@router.post(
    "/update",
    response_model=list[TemperatureRead],
)
async def update_temperatures(
    db: AsyncSession = Depends(get_db),
) -> list[Temperature]:
    result = await db.execute(select(City))
    cities = result.scalars().all()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            temperatures = await asyncio.gather(
                *[
                    fetch_temperature_for_city(city, client)
                    for city in cities
                ]
            )
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to update temperatures: {exc}",
        ) from exc

    db.add_all(temperatures)
    await db.commit()

    for temperature in temperatures:
        await db.refresh(temperature)

    return temperatures
