"""Temperature update and history endpoints."""

import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.weather import WeatherService, WeatherServiceError, get_weather_service


router = APIRouter(prefix="/temperatures", tags=["temperatures"])
DatabaseSession = Annotated[Session, Depends(get_db)]
WeatherServiceDependency = Annotated[WeatherService, Depends(get_weather_service)]


@router.post(
    "/update",
    response_model=list[schemas.Temperature],
    status_code=status.HTTP_201_CREATED,
)
async def update_temperatures(
    db: DatabaseSession,
    weather_service: WeatherServiceDependency,
) -> list[models.Temperature]:
    cities = list(db.scalars(select(models.City).order_by(models.City.id)))
    try:
        readings = await asyncio.gather(
            *(weather_service.fetch_current_temperature(city.name) for city in cities)
        )
    except WeatherServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    temperatures = [
        models.Temperature(
            city_id=city.id,
            date_time=reading.date_time,
            temperature=reading.temperature,
        )
        for city, reading in zip(cities, readings, strict=True)
    ]
    db.add_all(temperatures)
    try:
        db.commit()
        for temperature in temperatures:
            db.refresh(temperature)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save temperature data",
        ) from exc
    return temperatures


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
    db: DatabaseSession,
    city_id: Annotated[int | None, Query(gt=0)] = None,
) -> list[models.Temperature]:
    statement = select(models.Temperature).order_by(models.Temperature.id)
    if city_id is not None:
        statement = statement.where(models.Temperature.city_id == city_id)
    return list(db.scalars(statement))
