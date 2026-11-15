from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status

from app import crud, schemas
from app.dependencies import DbSession
from app.services.weather import WeatherServiceError, fetch_temperatures_for_cities

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post(
    "/update",
    response_model=schemas.TemperatureUpdateResult,
)
async def update_temperatures(db: DbSession) -> schemas.TemperatureUpdateResult:
    cities = crud.get_cities(db)
    if not cities:
        return schemas.TemperatureUpdateResult(temperatures=[], errors=[])

    city_pairs = [(city.id, city.name) for city in cities]
    try:
        results = await fetch_temperatures_for_cities(city_pairs)
    except WeatherServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    records: list[tuple[int, datetime, float]] = []
    errors: list[str] = []
    for result in results:
        if result.error:
            errors.append(result.error)
            continue
        if result.reading is None:
            errors.append(f"No weather data for '{result.city_name}'")
            continue
        records.append(
            (
                result.city_id,
                result.reading.date_time,
                result.reading.temperature,
            )
        )

    created = crud.create_temperatures(db, records) if records else []
    return schemas.TemperatureUpdateResult(
        temperatures=created,
        errors=errors,
    )


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
    db: DbSession,
    city_id: int | None = Query(default=None),
) -> list[schemas.Temperature]:
    if city_id is not None and crud.get_city(db, city_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id={city_id} not found",
        )
    return crud.get_temperatures(db, city_id=city_id)
