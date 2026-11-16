"""Temperature update and history endpoints."""

import asyncio
import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import City, Temperature
from app.schemas import (
    TemperatureRead,
    TemperatureUpdateFailure,
    TemperatureUpdateResult,
)
from app.services.weather import WeatherDataError, WeatherReading, fetch_current_temperature


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/temperatures", tags=["temperatures"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/update", response_model=TemperatureUpdateResult)
async def update_temperatures(session: SessionDep) -> TemperatureUpdateResult:
    """Fetch and store the current temperature for each city."""
    cities = list((await session.scalars(select(City).order_by(City.id))).all())
    if not cities:
        return TemperatureUpdateResult(updated_count=0, failed_count=0, failures=[])

    semaphore = asyncio.Semaphore(10)

    async def fetch_for_city(
        city: City,
        client: httpx.AsyncClient,
    ) -> tuple[City, WeatherReading | None, str | None]:
        async with semaphore:
            try:
                reading = await fetch_current_temperature(city.name, client)
                return city, reading, None
            except WeatherDataError as exc:
                return city, None, str(exc)
            except Exception:
                logger.exception("Unexpected weather update error for city_id=%s", city.id)
                return city, None, "Unexpected error while fetching weather data"

    async with httpx.AsyncClient(timeout=15.0) as client:
        results = await asyncio.gather(*(fetch_for_city(city, client) for city in cities))

    failures: list[TemperatureUpdateFailure] = []
    records: list[Temperature] = []
    for city, reading, error in results:
        if error is not None:
            failures.append(
                TemperatureUpdateFailure(
                    city_id=city.id,
                    city_name=city.name,
                    reason=error,
                )
            )
        elif reading is not None:
            records.append(
                Temperature(
                    city_id=city.id,
                    date_time=reading.date_time,
                    temperature=reading.temperature,
                )
            )

    if records:
        session.add_all(records)
        await session.commit()

    return TemperatureUpdateResult(
        updated_count=len(records),
        failed_count=len(failures),
        failures=failures,
    )


@router.get("", response_model=list[TemperatureRead])
async def list_temperatures(
    session: SessionDep,
    city_id: Annotated[int | None, Query(gt=0)] = None,
) -> list[Temperature]:
    """List all temperature readings, optionally filtered by city."""
    query = select(Temperature).order_by(Temperature.date_time.desc(), Temperature.id.desc())
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    result = await session.scalars(query)
    return list(result.all())

