from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from weather_app.app import crud, schemas
from weather_app.app.config import get_settings
from weather_app.app.database import get_db
from weather_app.app.services.weather import WeatherFetchError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    settings = get_settings()

    cities = crud.get_cities(db, limit=10_000)
    if not cities:
        raise HTTPException(
            status_code=400,
            detail="No cities in the database yet. Create one via POST /cities first.",
        )

    created_records: list[schemas.Temperature] = []
    failed: list[str] = []

    async with httpx.AsyncClient(
        timeout=settings.weather_request_timeout_seconds
    ) as client:
        for city in cities:
            try:
                temperature, observed_at = await fetch_current_temperature(
                    client, city.name
                )
            except (WeatherFetchError, httpx.HTTPError) as exc:
                failed.append(f"{city.name}: {exc}")
                continue

            db_record = crud.create_temperature(
                db,
                schemas.TemperatureCreate(
                    city_id=city.id,
                    date_time=observed_at,
                    temperature=temperature,
                ),
            )
            created_records.append(schemas.Temperature.model_validate(db_record))

    return schemas.TemperatureUpdateResult(
        updated=len(created_records),
        failed=failed,
        records=created_records,
    )


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
    city_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None and crud.get_city(db, city_id) is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
