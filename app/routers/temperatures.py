import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.services.weather import get_current_temperature


router = APIRouter(
    prefix='/temperatures',
    tags=['Temperatures'],
)


@router.post(
    '/update',
    response_model=list[schemas.TemperatureResponse],
)
async def update_temperatures(
    db: Session = Depends(get_db),
) -> list[schemas.TemperatureResponse]:
    cities = crud.get_cities(db)

    if not cities:
        return []

    async def fetch_temperature(
        city: models.City,
    ) -> tuple[models.City, float, str]:
        temperature, date_time = await get_current_temperature(
            latitude=city.latitude,
            longitude=city.longitude,
        )

        return city, temperature, date_time

    try:
        results = await asyncio.gather(
            *(fetch_temperature(city) for city in cities),
        )
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f'Failed to fetch weather data: {error}',
        ) from error

    temperature_records = []

    for city, temperature, date_time in results:
        temperature_record = crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=temperature,
            date_time=datetime.fromisoformat(date_time),
        )

        temperature_records.append(temperature_record)

    return temperature_records


@router.get(
    '',
    response_model=list[schemas.TemperatureResponse],
)
def read_temperatures(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[schemas.TemperatureResponse]:
    return crud.get_temperatures(
        db=db,
        city_id=city_id,
    )
