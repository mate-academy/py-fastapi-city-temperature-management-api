import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from city import crud as city_crud
from dependencies import get_db, get_http_client
from temperature import crud, schemas
from temperature.utils import get_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None, db: Session = Depends(get_db)
):
    if (
        city_id is not None
        and city_crud.get_city_by_id(db=db, city_id=city_id) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(
    db: Session = Depends(get_db),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    cities = city_crud.get_all_cities(db=db)

    current_temperatures = await asyncio.gather(
        *(get_current_temperature(client, city.name) for city in cities)
    )

    new_temperatures = []
    failed_cities = []
    for city, current_temperature in zip(cities, current_temperatures):
        if current_temperature is None:
            failed_cities.append(city.name)
            continue

        new_temperatures.append(
            schemas.TemperatureCreate(
                city_id=city.id, temperature=current_temperature
            )
        )

    return schemas.TemperatureUpdateResult(
        updated=crud.create_temperatures(db=db, temperatures=new_temperatures),
        failed_cities=failed_cities,
    )
