from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from db.session import get_db
from city import crud as city_crud
from temperature.crud import (
    get_temperatures,
    get_temperature_for_city, update_temperatures,

)
from temperature.exceptions import TemperatureNotFound
from temperature.schema import TemperatureRead
from services.weather import get_weather, WeatherServiceError


router = APIRouter()


@router.get("/temperatures/", response_model=List[TemperatureRead])
def get_all_temperatures(
    db: Annotated[Session, Depends(get_db)],
    city_id: int | None = None,
):
    try:
        if city_id:
            return get_temperature_for_city(db, city_id)
        return get_temperatures(db)
    except TemperatureNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/temperature/update", response_model=List[TemperatureRead])
async def update_temperatures_for_all_cities(
    db: Annotated[Session, Depends(get_db)]
):
    cities = city_crud.get_all_cities(db)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    results = []

    for city in cities:
        try:
            temp = await get_weather(city.name)
            obj = update_temperatures(db, city.id, temp)
            results.append(obj)
        except WeatherServiceError as e:
            continue
        except Exception:
            raise HTTPException(
                status_code=500, detail="Database error while saving temperature"
            )

    if not results:
        raise HTTPException(
            status_code=502,
            detail="Could not fetch temperature data for any city",
        )

    return results
