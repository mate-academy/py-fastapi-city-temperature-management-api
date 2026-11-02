from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.city import crud as city_crud
from src.dependencies import get_db
from src.settings import settings
from src.temperature import crud, schemas
from src.temperature.services import fetch_temperatures

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    if not settings.weather_api_key:
        raise HTTPException(status_code=500, detail="WEATHER_API_KEY is not configured")

    cities = city_crud.get_cities(db, limit=None)
    if not cities:
        return schemas.TemperatureUpdateResult(updated=0, failed=[])

    values = await fetch_temperatures([city.name for city in cities])
    now = datetime.now(timezone.utc)

    new_records = []
    failed = []
    for city, value in zip(cities, values):
        if value is None:
            failed.append(city.name)
        else:
            new_records.append(
                schemas.TemperatureCreate(city_id=city.id, date_time=now, temperature=value)
            )

    crud.create_temperatures(db, new_records)
    return schemas.TemperatureUpdateResult(updated=len(new_records), failed=failed)


@router.get("/", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None and city_crud.get_city(db, city_id) is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
