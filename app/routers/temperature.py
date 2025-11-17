from typing import Any
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from datetime import datetime
import httpx

from app.dependencies import get_db
from app.schemas.temperature import (
    TemperatureCreate,
    Temperature
)
from app.crud.temperature import (
    create_temperature,
    get_temperatures
)
from app.crud.city import get_cities


router = APIRouter()
@router.get("/temperatures", response_model=list[Temperature])
def temperatures_get(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> Any:
    return get_temperatures(db, city_id, skip, limit)


@router.post("/temperatures/update", response_model=list[Temperature])
async def temperatures_update(db: Session = Depends(get_db)):
    cities = await run_in_threadpool(get_cities, db)

    created = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(f"https://wttr.in/{city.name}?format=j1")
            data = response.json()
            temp_c = float(data["current_condition"][0]["temp_C"])

            temp_create = TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp_c,
            )

            temp_db = await run_in_threadpool(create_temperature, db, temp_create)
            created.append(temp_db)

    return created
