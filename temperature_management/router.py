import asyncio
from typing import Annotated, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from temperature_management import crud
from dependies import get_db
from temperature_management import schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(
        db: Annotated[Session, Depends(get_db)]
):
    return crud.get_all_cities(db=db)

@router.post("/cities/", response_model=schemas.City)
def create_city(
        db: Annotated[Session, Depends(get_db)],
        city_info: schemas.CityCreate
):
    return crud.create_city(
        db=db,
        city_info=city_info
    )

@router.get("/cities/{city_id}/", response_model=schemas.City)
def get_city_by_id(
        db: Annotated[Session, Depends(get_db)],
        city_id: int
):
    return crud.get_city_by_id(
        db=db,
        city_id=city_id
    )


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(
        db: Annotated[Session, Depends(get_db)],
        city_id: int
):
    return crud.delete_city_by_id(
        db=db,
        city_id=city_id
    )

@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
        db: Annotated[Session, Depends(get_db)],
        city_id: int,
        city_update_info: schemas.CityUpdate
):
    return crud.update_city(
        db=db,
        city_id=city_id,
        city_update_info=city_update_info
    )

@router.patch("/cities/{city_id}/", response_model=schemas.City)
def partial_update_city(
        db: Annotated[Session, Depends(get_db)],
        city_id: int,
        city_update_info: schemas.CityPartialUpdate
):
    return crud.partial_update_city(
        db=db,
        city_id=city_id,
        city_update_info=city_update_info
    )

@router.post("/temperatures/update/", status_code=status.HTTP_201_CREATED)
def fetch_new_temperature(
        db: Annotated[Session, Depends(get_db)]
):
    return asyncio.run(crud.fetch_temperature(db=db))


@router.get("/temperatures/", response_model=Union[list[schemas.Temperature], schemas.CityWithTemperatures])
def read_temperatures(
        db: Annotated[Session, Depends(get_db)],
        city_id: int | None = None
):
    if city_id:
        return crud.get_temperatures_by_id(db=db, city_id=city_id)
    return crud.get_all_temperatures(db=db)
