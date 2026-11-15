import asyncio

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cities import crud as cities_crud
from app.dependencies import get_db
from app.temperatures import crud, schemas, service

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)) -> dict:
    cities = cities_crud.get_cities(db)

    async with httpx.AsyncClient(timeout=10) as client:
        results = await asyncio.gather(
            *(service.fetch_temperature(client, city.name)
              for city in cities)
        )

    updated, failed = 0, []
    for city, temperature in zip(cities, results):
        if temperature is None:
            failed.append(city.name)
            continue
        crud.create_temperature(db, city.id, temperature)
        updated += 1

    return {"updated": updated, "failed": failed}


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
        city_id: int | None = None,
        db: Session = Depends(get_db)
) -> list[schemas.Temperature]:
    return crud.get_temperatures(db, city_id)
