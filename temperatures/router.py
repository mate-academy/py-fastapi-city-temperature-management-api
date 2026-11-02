from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from cities import crud as cities_crud
from dependencies import DbSession
from schemas.temperature import (
    Temperature,
    TemperatureCreate,
    TemperatureUpdateError,
    TemperatureUpdateResult,
)
from temperatures import crud
from temperatures.weather import WeatherAPIError, fetch_temperatures

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=TemperatureUpdateResult)
async def update_temperatures(db: DbSession):
    """Fetch the current temperature for every city and store it."""
    cities = cities_crud.get_all_cities(db=db)
    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities in the database. Add a city first.",
        )

    results = await fetch_temperatures([city.name for city in cities])

    new_records: list[TemperatureCreate] = []
    failed: list[TemperatureUpdateError] = []
    for city, result in zip(cities, results, strict=True):
        if isinstance(result, BaseException):
            if isinstance(result, WeatherAPIError):
                detail = str(result)
            else:
                detail = "Unexpected error"
            failed.append(
                TemperatureUpdateError(
                    city_id=city.id, city_name=city.name, detail=detail
                )
            )
            continue
        date_time, temperature = result
        new_records.append(
            TemperatureCreate(
                city_id=city.id, date_time=date_time, temperature=temperature
            )
        )

    if not new_records:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Could not fetch temperature for any city",
                "failed": [f.model_dump() for f in failed],
            },
        )

    updated = crud.create_temperatures(db=db, temperatures=new_records)
    return TemperatureUpdateResult(updated=updated, failed=failed)


@router.get("/", response_model=list[Temperature])
def list_temperatures(
    db: DbSession,
    city_id: Annotated[
        int | None, Query(description="Only return records for this city")
    ] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    city_missing = (
        city_id is not None
        and cities_crud.get_city(db=db, city_id=city_id) is None
    )
    if city_missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )
    return crud.get_temperatures(
        db=db, city_id=city_id, skip=skip, limit=limit
    )
