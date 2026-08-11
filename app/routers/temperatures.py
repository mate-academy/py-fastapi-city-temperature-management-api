from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import city as city_crud
from app.crud import temperature as temperature_crud
from app.database import get_database
from app.models.temperature import Temperature
from app.schemas.temperature import TemperatureCreate, TemperatureRead
from app.services.weather import WeatherServiceError, fetch_current_temperature


router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("/", response_model=list[TemperatureRead])
def get_temperatures(
    database: Annotated[Session, Depends(get_database)],
    city_id: int | None = None,
) -> list[Temperature]:
    return temperature_crud.get_temperatures(
        db=database,
        city_id=city_id,
    )


@router.post("/update", response_model=list[TemperatureRead])
async def update_temperatures(
    database: Annotated[Session, Depends(get_database)],
) -> list[Temperature]:
    cities = city_crud.get_cities(database)

    try:
        created_temperatures = []

        for city in cities:
            current_temperature = await fetch_current_temperature(city.name)

            temperature_in = TemperatureCreate(
                date_time=datetime.now(timezone.utc),
                temperature=current_temperature,
            )

            temperature = temperature_crud.create_temperature(
                database=database,
                temperature=temperature_in,
                city_id=city.id,
            )
            created_temperatures.append(temperature)

        return created_temperatures

    except WeatherServiceError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
