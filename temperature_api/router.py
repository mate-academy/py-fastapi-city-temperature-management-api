from fastapi import APIRouter, Depends, HTTPException, Query, status
import httpx
from sqlalchemy.orm import Session

from city_crud_api.api.crud import get_all_cities
from db.engine import get_db
from temperature_api import schemas, crud
from temperature_api.get_temp import get_temp

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.get(
    "",
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
    status_code=status.HTTP_201_CREATED,
)
async def update_temperatures(
    db: Session = Depends(get_db),
):
    cities = get_all_cities(db)

    values = []

    for city in cities:
        try:
            values.append(await get_temp(city.name))
        except (httpx.HTTPError, RuntimeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Could not update {city.name}: {exc}",
            ) from None

    records = [
        crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature_value=value,
        )
        for city, value in zip(cities, values)
    ]

    return records
