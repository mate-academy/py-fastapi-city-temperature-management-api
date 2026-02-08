import asyncio

import datetime

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from dependencies import get_db

from city.models import City
from city import crud as city_crud

from temperature import crud, schemas
from temperature.crud import fetch_current_temperature_celsius
from temperature.models import Temperature

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities: list[City] = db.scalars(select(City)).all()

    async def _fetch_for_city(city: City):
        temp_c = await fetch_current_temperature_celsius(city.name)
        return city, temp_c

    tasks = [asyncio.create_task(_fetch_for_city(city)) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    now = datetime.datetime.utcnow()

    added = 0
    failed: list[dict[str, Any]] = []

    for city, result in zip(cities, results, strict=False):
        if isinstance(result, Exception):
            failed.append(
                {"city_id": city.id, "city_name": city.name, "error": str(result)}
            )
            continue

        _city, temp_c = result
        db.add(
            Temperature(
                city_id=_city.id,
                date_time=now,
                temperature=temp_c,
            )
        )
        added += 1

    db.commit()

    return {
        "cities_total": len(cities),
        "records_added": added,
        "failed": failed,
    }


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None:
        city = city_crud.get_city_by_id(db, city_id)
        if city is None:
            raise HTTPException(status_code=404, detail="City not found")

    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
