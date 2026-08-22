"""Temperature update and history endpoints."""
import asyncio
from datetime import datetime, timezone
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.weather import WeatherLookupError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


async def _fetch_for_city(client: httpx.AsyncClient, city) -> dict:
    """Fetch the current temperature for one city, capturing failures instead
    of letting one bad city abort the whole batch."""
    try:
        temperature = await fetch_current_temperature(client, city.name)
        return {"city_id": city.id, "temperature": temperature, "error": None}
    except (WeatherLookupError, httpx.HTTPError) as exc:
        return {"city_id": city.id, "temperature": None, "error": str(exc)}


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    """
    Fetch the current temperature for every city in the database from an
    online weather API (Open-Meteo) and persist the readings.

    Requests for all cities are fired concurrently. A failure for one city
    (e.g. it can't be geocoded) does not prevent the others from succeeding;
    it's reported back in the `failed` list instead.
    """
    cities = crud.get_cities(db, skip=0, limit=10_000)

    updated: list = []
    failed: list = []

    if cities:
        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(
                *(_fetch_for_city(client, city) for city in cities)
            )

        now = datetime.now(timezone.utc)
        for result in results:
            if result["error"] is not None:
                failed.append({"city_id": result["city_id"], "reason": result["error"]})
                continue
            db_temp = crud.create_temperature(
                db,
                city_id=result["city_id"],
                date_time=now,
                temperature=result["temperature"],
            )
            updated.append(db_temp)

    return schemas.TemperatureUpdateResult(updated=updated, failed=failed)


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
    city_id: Optional[int] = Query(
        None, description="Filter temperature history by city id"
    ),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get temperature history.

    - `GET /temperatures` returns all records.
    - `GET /temperatures?city_id={id}` returns records for one city only.
    """
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
