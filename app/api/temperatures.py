import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.services.weather_client import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


def parse_coords(additional_info: str | None) -> tuple[float, float] | None:
    if not additional_info:
        return None
    parts = [p.strip() for p in additional_info.split(",")]
    if len(parts) != 2:
        return None
    try:
        return float(parts[0]), float(parts[1])
    except ValueError:
        return None


@router.get("", response_model=list[schemas.TemperatureRead])
def get_temperatures(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_temperatures(db, city_id=city_id)


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=400, detail="No cities found")

    tasks: list = []
    valid_cities: list[models.City] = []

    for city in cities:
        coords = parse_coords(city.additional_info)
        if not coords:
            continue
        lat, lon = coords
        tasks.append(fetch_temperature(lat, lon))
        valid_cities.append(city)

    if not tasks:
        raise HTTPException(status_code=400, detail="No cities with valid coordinates")

    results = await asyncio.gather(*tasks, return_exceptions=True)

    updated = 0
    skipped = 0

    for city, result in zip(valid_cities, results):
        if isinstance(result, Exception):
            skipped += 1
            continue
        crud.create_temperature(db, city.id, float(result))
        updated += 1

    return {"updated": updated, "skipped": skipped}
