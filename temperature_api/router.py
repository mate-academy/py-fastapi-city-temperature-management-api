from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import asyncio

from city_crud_api.api.crud import get_all_cities
from db.engine import get_db
from temperature_api import schemas, crud
from temperature_api.get_temp import get_temp

router = APIRouter(
    prefix="/temperature",
    tags=["Temperature"],
)


@router.get(
    "/",
    response_model=list[schemas.Temperature],
)
def read_temperatures(
    db: Session = Depends(get_db),
    city_id: int | None = Query(default=None),
):
    if city_id is not None:
        return crud.get_temperature_for_city(
            db=db,
            city_id=city_id,
        )

    return crud.get_all_temperatures(db=db)


@router.post(
    "/update",
    response_model=list[schemas.Temperature],
)
async def update_temperatures(
    db: Session = Depends(get_db),
):
    cities = get_all_cities(db)

    values = await asyncio.gather(*(get_temp(city.name) for city in cities))

    records = [
        crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature_value=value,
        )
        for city, value in zip(cities, values)
    ]

    return records
