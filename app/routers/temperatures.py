import asyncio
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.services.weather import (
    WeatherServiceError,
    get_current_temperature,
)


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


async def fetch_temperature(
    client: httpx.AsyncClient,
    city: models.City,
) -> tuple[models.City, float | Exception]:
    try:
        temperature = await get_current_temperature(
            client=client,
            city_name=city.name,
        )

        return city, temperature

    except (httpx.HTTPError, WeatherServiceError) as error:
        return city, error


@router.post(
    "/update",
    response_model=list[schemas.Temperature],
)
async def update_temperatures(
    db: Session = Depends(get_db),
):
    cities = crud.get_cities(db=db)

    if not cities:
        raise HTTPException(
            status_code=400,
            detail="No cities found",
        )

    async with httpx.AsyncClient(
        timeout=10.0,
    ) as client:
        tasks = [
            fetch_temperature(
                client=client,
                city=city,
            )
            for city in cities
        ]

        results = await asyncio.gather(*tasks)

    temperature_records = []

    for city, result in results:
        if isinstance(result, Exception):
            continue

        temperature_record = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=result,
        )

        db.add(temperature_record)
        temperature_records.append(
            temperature_record
        )

    if not temperature_records:
        raise HTTPException(
            status_code=502,
            detail="Could not fetch temperature data",
        )

    db.commit()

    for record in temperature_records:
        db.refresh(record)

    return temperature_records


@router.get(
    "",
    response_model=list[schemas.Temperature],
)
def get_temperatures(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if city_id is not None:
        city = crud.get_city(
            db=db,
            city_id=city_id,
        )

        if city is None:
            raise HTTPException(
                status_code=404,
                detail="City not found",
            )

    return crud.get_temperatures(
        db=db,
        city_id=city_id,
    )
