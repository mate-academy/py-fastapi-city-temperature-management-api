import asyncio
from datetime import datetime, timezone
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, DbSession
from app.weather import get_current_temperature


router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("", response_model=list[schemas.Temperature])
@router.get("/", response_model=list[schemas.Temperature], include_in_schema=False)
def get_temperatures(
    db: DbSession, city_id: int | None = None
) -> list[models.Temperature]:
    """List all temperature records, optionally only those of one city."""
    query = select(models.Temperature).order_by(
        models.Temperature.date_time, models.Temperature.id
    )

    if city_id is not None:
        if db.get(models.City, city_id) is None:
            raise HTTPException(status_code=404, detail="City not found")
        query = query.where(models.Temperature.city_id == city_id)

    return list(db.scalars(query).all())


@router.post("/update")
async def update_temperatures(db: DbSession) -> dict:
    """Fetch the current temperature of every city and store it.

    Cities that cannot be fetched are skipped and reported under "failed".
    """
    cities = list(db.scalars(select(models.City)).all())
    if not cities:
        return {"updated": 0, "failed": [], "message": "No cities in the database"}

    async with httpx.AsyncClient(timeout=10) as client:
        results = await asyncio.gather(
            *(get_current_temperature(client, city.name) for city in cities),
            return_exceptions=True,
        )

    now = datetime.now(timezone.utc)
    records: list[models.Temperature] = []
    failed: list[dict[str, str]] = []

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            failed.append(
                {"city": city.name, "reason": str(result) or type(result).__name__}
            )
        else:
            records.append(
                models.Temperature(
                    city_id=city.id, date_time=now, temperature=result
                )
            )

    db.add_all(records)
    db.commit()

    return {"updated": len(records), "failed": failed}
