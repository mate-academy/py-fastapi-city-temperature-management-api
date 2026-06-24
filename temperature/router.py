from datetime import datetime
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city import crud as city_crud
from dependencies import get_db
from temperature import crud, schemas

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1},
        )
        results = geo.json().get("results")
        if not results:
            return None
        lat = results[0]["latitude"]
        lon = results[0]["longitude"]

        weather = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current": "temperature_2m"},
        )
        return weather.json()["current"]["temperature_2m"]


@router.post("/update")
async def update_temperatures(db: Annotated[Session, Depends(get_db)]):
    cities = city_crud.get_cities(db)
    created = []
    for city in cities:
        temp_value = await fetch_temperature(city.name)
        if temp_value is None:
            continue
        record = schemas.TemperatureBase(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temp_value,
        )
        created.append(crud.create_temperature(db, record))
    return {"updated": len(created)}


@router.get("/", response_model=list[schemas.Temperature])
def read_temperatures(
    skip: int = 0, limit: int = 100, city_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db, skip=skip, limit=limit, city_id=city_id)
