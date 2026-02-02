import asyncio
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import city as city_crud
from app.crud import temperature as temp_crud
from app.db.session import get_session
from app.models import Temperature
from app.schemas.temperature import TemperatureRead, TemperatureUpdateResult
from app.services.temperature_provider import fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("", response_model=list[TemperatureRead])
async def list_temperatures(
    city_id: int | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[Temperature]:
    if city_id is not None:
        city = await city_crud.get_city(session, city_id)
        if city is None:
            raise HTTPException(status_code=404, detail="City not found.")

    return await temp_crud.list_temperatures(session, city_id=city_id)


@router.post("/update", response_model=TemperatureUpdateResult)
async def update_temperatures(
        session: AsyncSession = Depends(get_session)
) -> TemperatureUpdateResult:
    cities = await city_crud.get_cities(session)
    if not cities:
        return TemperatureUpdateResult(total_cities=0, stored=0, failed_city_ids=[])

    sem = asyncio.Semaphore(10)

    async with httpx.AsyncClient(timeout=10) as client:

        async def _one(city_id: int, city_name: str) -> tuple[int, float]:
            async with sem:
                temp_value = await fetch_current_temperature(city_name, client)
                return city_id, temp_value

        tasks = [_one(c.id, c.name) for c in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    now = datetime.now(timezone.utc)

    failed: list[int] = []
    records: list[Temperature] = []

    for city_obj, res in zip(cities, results, strict=True):
        if isinstance(res, Exception):
            failed.append(city_obj.id)
            continue
        city_id, temp_value = res
        records.append(Temperature(city_id=city_id, date_time=now, temperature=temp_value))

    if records:
        session.add_all(records)
        await session.commit()

    return TemperatureUpdateResult(
        total_cities=len(cities),
        stored=len(records),
        failed_city_ids=failed,
    )
