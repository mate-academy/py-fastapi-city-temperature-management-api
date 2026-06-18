from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import TemperatureBase, TemperatureResponse, TemperatureUpdateResponse
from app.services.weather import fetch_all_city_temperatures
import app.crud.city as city_crud
import app.crud.temperature as temp_crud

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=TemperatureUpdateResponse)
async def update_temperatures(db: Session = Depends(get_db)):
    """
    Fetch the current temperature for every city in the database and persist
    the results as new Temperature records.

    Returns a summary with counts of successes / failures and the saved records.
    """
    cities = city_crud.get_cities(db, limit=10_000)
    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in the database. Add cities first.",
        )

    # Fetch all temperatures concurrently
    results = await fetch_all_city_temperatures([c.name for c in cities])

    name_to_id = {c.name: c.id for c in cities}
    saved: list[TemperatureResponse] = []
    failed = 0

    for city_name, (temperature, recorded_at) in results.items():
        if temperature is None:
            failed += 1
            continue
        record = TemperatureBase(
            city_id=name_to_id[city_name],
            date_time=recorded_at,
            temperature=temperature,
        )
        db_record = temp_crud.create_temperature(db, record)
        saved.append(TemperatureResponse.model_validate(db_record))

    return TemperatureUpdateResponse(updated=len(saved), failed=failed, records=saved)


@router.get("/", response_model=list[TemperatureResponse])
def list_temperatures(
    city_id: int | None = Query(None, description="Filter by city ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=5000),
    db: Session = Depends(get_db),
):
    """
    Return temperature records, newest first.
    Optionally filter by `city_id` via query parameter.
    """
    if city_id is not None:
        # Validate that the city exists
        city = city_crud.get_city(db, city_id)
        if city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with id={city_id} not found.",
            )
    return temp_crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)