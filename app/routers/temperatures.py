from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import city as city_crud
from app.crud import temperature as temperature_crud
from app.database import get_db
from app.schemas.temperature import Temperature, TemperatureUpdateResult
from app.services.weather import fetch_temperatures_for_cities

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", response_model=TemperatureUpdateResult)
async def update_temperatures(
    db: Session = Depends(get_db),
) -> TemperatureUpdateResult:
    cities = city_crud.get_cities(db)
    if not cities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No cities found in the database",
        )

    weather_results = await fetch_temperatures_for_cities(
        [city.name for city in cities]
    )

    created_records = 0
    failed_cities: list[str] = []

    for city in cities:
        result = weather_results[city.name]
        if isinstance(result, Exception):
            failed_cities.append(city.name)
            continue

        temperature_crud.create_temperature(
            db=db,
            city_id=city.id,
            date_time=result.date_time,
            temperature=result.temperature,
        )
        created_records += 1

    db.commit()

    if created_records == 0:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not fetch temperature for any city",
        )

    return TemperatureUpdateResult(
        created_records=created_records,
        failed_cities=failed_cities,
    )


@router.get("", response_model=list[Temperature])
def list_temperatures(
    city_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
) -> list[Temperature]:
    if city_id is not None and city_crud.get_city(db, city_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return temperature_crud.get_temperatures(db, city_id)
