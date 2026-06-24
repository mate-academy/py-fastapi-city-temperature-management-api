from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.weather_service import get_temperatures_for_cities

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post(
    "/update",
    response_model=schemas.TemperatureUpdateResult,
    status_code=status.HTTP_200_OK,
)
async def update_temperatures(db: Session = Depends(get_db)):
    """
    Fetch the current temperature for every city in the database from Open-Meteo
    and persist the results. Returns a summary of successful and failed lookups.
    """
    cities: list[models.City] = crud.get_cities(db, limit=1000)
    if not cities:
        return schemas.TemperatureUpdateResult(
            updated=0,
            failed=[],
            message="No cities in the database.",
        )

    name_to_id = {city.name: city.id for city in cities}
    temperatures = await get_temperatures_for_cities(list(name_to_id.keys()))

    now = datetime.utcnow()
    updated_count = 0
    failed: list[str] = []

    for city_name, temp in temperatures.items():
        if temp is None:
            failed.append(city_name)
            continue
        record = models.Temperature(
            city_id=name_to_id[city_name],
            date_time=now,
            temperature=temp,
        )
        db.add(record)
        updated_count += 1

    db.commit()

    return schemas.TemperatureUpdateResult(
        updated=updated_count,
        failed=failed,
        message=f"Updated {updated_count} cities. {len(failed)} failed.",
    )


@router.get("/", response_model=list[schemas.TemperatureResponse])
def list_temperatures(
    city_id: int | None = Query(default=None, description="Filter by city ID"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Return temperature history records, optionally filtered by city_id.
    Supports pagination via skip/limit.
    """
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).offset(skip).limit(limit).all()
