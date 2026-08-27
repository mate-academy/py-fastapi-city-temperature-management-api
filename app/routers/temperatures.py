import asyncio

import httpx
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services import WeatherServiceError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(
    db: Session = Depends(get_db),
) -> schemas.TemperatureUpdateResult:
    cities = list(db.scalars(select(models.City).order_by(models.City.id)))
    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            *(fetch_current_temperature(client, city.name) for city in cities),
            return_exceptions=True,
        )

    created: list[models.Temperature] = []
    errors: dict[int, str] = {}
    for city, result in zip(cities, results, strict=True):
        if isinstance(result, BaseException):
            errors[city.id] = (
                str(result) if isinstance(result, WeatherServiceError) else "Unexpected error"
            )
            continue
        record = models.Temperature(
            city_id=city.id,
            date_time=result.date_time,
            temperature=result.temperature,
        )
        db.add(record)
        created.append(record)

    db.commit()
    for record in created:
        db.refresh(record)
    return schemas.TemperatureUpdateResult(created=created, errors=errors)


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
    city_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
) -> list[models.Temperature]:
    query = select(models.Temperature).order_by(
        models.Temperature.date_time.desc(), models.Temperature.id.desc()
    )
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    return list(db.scalars(query))
