import asyncio
from typing import List, Optional, Sequence, Tuple

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import crud as city_crud
from app.city.models import City
from app.temperature import models, schemas
from app.temperature.weather import (
    WeatherServiceError,
    fetch_current_temperature,
)


async def get_temperatures(
    db: AsyncSession,
    city_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[models.Temperature]:
    query = select(models.Temperature)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    query = (
        query.order_by(
            models.Temperature.date_time.desc(), models.Temperature.id.desc()
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def _fetch_for_city(
    client: httpx.AsyncClient, city: City
) -> Tuple[City, object]:
    try:
        return city, await fetch_current_temperature(client, city.name)
    except WeatherServiceError as exc:
        return city, exc


async def update_temperatures(
    db: AsyncSession, client: httpx.AsyncClient
) -> schemas.TemperatureUpdateResult:
    """Fetch current temperatures for all cities concurrently and store them.

    A failure for one city does not prevent the others from being saved.
    """
    cities = await city_crud.get_all_cities(db)
    results = await asyncio.gather(
        *(_fetch_for_city(client, city) for city in cities)
    )

    created: List[models.Temperature] = []
    failed: List[schemas.FailedCity] = []
    for city, outcome in results:
        if isinstance(outcome, WeatherServiceError):
            failed.append(
                schemas.FailedCity(
                    city_id=city.id, city_name=city.name, reason=str(outcome)
                )
            )
            continue
        date_time, temperature = outcome
        record = models.Temperature(
            city_id=city.id, date_time=date_time, temperature=temperature
        )
        db.add(record)
        created.append(record)

    await db.commit()
    return schemas.TemperatureUpdateResult(
        updated=[schemas.Temperature.model_validate(t) for t in created],
        failed=failed,
    )
