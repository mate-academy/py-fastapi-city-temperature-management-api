from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import schemas, models, crud

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db)]


@router.post("/cities/", response_model=schemas.City)
def create_city(db: SessionDep, city: schemas.CityCreate) -> models.City:
    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: SessionDep) -> list[models.City]:
    return crud.get_city_list(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(db: SessionDep, city_id: int) -> models.City:
    return crud.get_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    db: SessionDep, city_id: int, city_data: schemas.CityCreate
) -> models.City:
    return crud.update_city(db=db, city_id=city_id, city_data=city_data)


@router.delete("/cities/{city_id}/")
def delete_city(db: SessionDep, city_id: int) -> dict[str, str]:
    return crud.delete_city(db=db, city_id=city_id)
