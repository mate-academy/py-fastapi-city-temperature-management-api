from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas

from dependencies import get_db


router = APIRouter(tags=["City Operations"])


def common_parameters(city_id: int, db: Session = Depends(get_db)):
    return {"city_id": city_id, "db": db}


CommonDeps = Depends(common_parameters)


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
) -> schemas.City:
    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=List[schemas.City])
def retrieve_cities(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[schemas.City]:
    return crud.get_all_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=schemas.City,)
def get_city(common: dict = CommonDeps) -> schemas.City:
    return crud.get_existing_city(db=common["db"], city_id=common["city_id"])


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city: schemas.CityUpdate,
    common: dict = CommonDeps
) -> schemas.City:
    return crud.update_city(
        db=common["db"],
        city=city,
        city_id=common["city_id"]
    )


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(common: dict = CommonDeps) -> schemas.City:
    return crud.delete_city(db=common["db"], city_id=common["city_id"])
