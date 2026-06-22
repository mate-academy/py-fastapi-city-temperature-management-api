from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.weather import WeatherLookupError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=list[schemas.Temperature], status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: Session = Depends(get_db)):
    """Fetch the current temperature for every city and store it as a new record."""
    cities = db.query(models.City).all()
    recorded_at = datetime.now(timezone.utc)
    new_records = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        for city in cities:
            try:
                temperature = await fetch_current_temperature(client, city.name)
            except (WeatherLookupError, httpx.HTTPError):
                continue

            db_temperature = models.Temperature(
                city_id=city.id, date_time=recorded_at, temperature=temperature
            )
            db.add(db_temperature)
            new_records.append(db_temperature)

    db.commit()
    for record in new_records:
        db.refresh(record)
    return new_records


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(city_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).all()
