import asyncio
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.weather import (
    get_city_coordinates,
    get_current_temperature,
)


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.post("/update", response_model=list[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.scalars(select(models.City)).all()

    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities found in the database",
        )

    async with httpx.AsyncClient(timeout=10.0) as client:

        async def fetch_temperature(city):
            latitude, longitude = await get_city_coordinates(
                client,
                city.name,
            )

            temperature = await get_current_temperature(
                client,
                latitude,
                longitude,
            )

            return city.id, temperature

        results = await asyncio.gather(
            *(fetch_temperature(city) for city in cities)
        )

    records = []

    for city_id, temperature in results:
        record = models.Temperature(
            city_id=city_id,
            temperature=temperature,
            date_time=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        db.add(record)
        records.append(record)

    db.commit()

    for record in records:
        db.refresh(record)

    return records


@router.get("", response_model=list[schemas.Temperature])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = select(models.Temperature)

    if city_id is not None:
        city = db.get(models.City, city_id)

        if city is None:
            raise HTTPException(
                status_code=404,
                detail="City not found",
            )

        query = query.where(
            models.Temperature.city_id == city_id
        )

    query = query.order_by(
        models.Temperature.date_time.desc()
    )

    return db.scalars(query).all()
