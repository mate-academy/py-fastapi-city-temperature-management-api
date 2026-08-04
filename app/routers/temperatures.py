import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import City as CityModel
from app.models import Temperature as TemperatureModel
from app.schemas import Temperature
from app.services.weather import fetch_current_temperature


router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)


@router.post(
    "/update",
    response_model=list[Temperature],
)
async def update_temperatures(
    database: Session = Depends(get_db),
):
    cities_query = select(CityModel)
    cities = database.scalars(cities_query).all()

    temperature_records = []

    for city in cities:
        try:
            date_time, temperature_value = (
                await fetch_current_temperature(
                    city.name
                )
            )
        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
        ) as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    f"Could not fetch temperature "
                    f"for {city.name}: {error}"
                ),
            ) from error

        temperature_record = TemperatureModel(
            city_id=city.id,
            date_time=date_time,
            temperature=temperature_value,
        )

        database.add(temperature_record)
        temperature_records.append(
            temperature_record
        )

    database.commit()

    for temperature_record in temperature_records:
        database.refresh(temperature_record)

    return temperature_records

@router.get(
    "",
    response_model=list[Temperature],
)
def get_temperatures(
    city_id: int | None = None,
    database: Session = Depends(get_db),
):
    query = select(TemperatureModel)

    if city_id is not None:
        query = query.where(
            TemperatureModel.city_id == city_id
        )

    temperature_records = database.scalars(
        query
    ).all()

    return temperature_records
