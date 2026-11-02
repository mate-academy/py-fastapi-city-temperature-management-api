from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cities.crud import get_city_by_id, get_cities
from database import get_db_session
from temperatures import schemas, crud, weather_client

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)


@router.post("/update/", response_model=list[schemas.ReadTemperatureSchema])
async def update_temperatures_for_all_cities(
        db_session: Annotated[Session, Depends(get_db_session)]
):
    cities = get_cities(db_session=db_session)
    city_temp_dict = await weather_client.fetch_temperatures(cities)
    return crud.create_temperatures(db_session, city_temp_dict)


@router.get("", response_model=list[schemas.ReadTemperatureSchema])
def read_temperatures(
        db_session: Annotated[Session, Depends(get_db_session)],
        city_id: int | None = None
):
    if city_id is not None:
        city_from_db = get_city_by_id(db_session=db_session, city_id=city_id)
        if city_from_db is None:
            raise HTTPException(status_code=404, detail="City not found")
    return crud.get_temperatures(db_session, city_id)
