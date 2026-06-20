from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from city import models as city_models
from dependencies import get_db
from temperature import crud, models, schemas
from weather import fetch_temperature

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db)]


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    db: SessionDep,
    city_id: int | None = None,
) -> list[models.Temperature]:
    return crud.get_temperature(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: SessionDep) -> list[models.Temperature]:
    cities = db.scalars(select(city_models.City)).all()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    temperature_records = []

    for city in cities:
        try:
            weather_data = await fetch_temperature(city.name)
        except httpx.HTTPError:
            raise HTTPException(
                status_code=500,
                detail=f"Could not fetch temperature for city '{city.name}'",
            )

        temperature_record = models.Temperature(
            city_id=city.id,
            temperature=weather_data["temperature"],
            date_time=weather_data["date_time"],
        )
        db.add(temperature_record)
        temperature_records.append(temperature_record)

    db.commit()

    for record in temperature_records:
        db.refresh(record)

    return temperature_records
