from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.orm import Session

from city_temp import crud
from city_temp.schemas import (
    City,
    CityCreate,
    CityDelete,
    CityUpdate,
)

import dependencies


router = APIRouter(prefix="/cities", tags=["cities"],)


@router.post("/", response_model=City)
def create_city(
        city_to_create: CityCreate,
        db: Session = Depends(dependencies.get_db),
):
    return crud.create_city(db=db, new_city=city_to_create)


@router.get("/", response_model=List[City])
def list_cities(
        db: Session = Depends(dependencies.get_db),
):
    return crud.list_cities(db=db)


@router.get("/{city_id}/", response_model=City)
def get_city(
        city_id: int,
        db: Session = Depends(dependencies.get_db),
):
    return crud.get_city(db=db, city_id=city_id)


@router.put("/{city_id}/", response_model=City)
def update_city(
        city_id: int,
        updated_city: CityUpdate,
        db: Session = Depends(dependencies.get_db),
):
    return crud.update_city(
        db=db,
        city_id=city_id,
        updated_city=updated_city
    )


@router.delete("/{city_id}/", response_model=CityDelete)
def delete_city(
        city_id: int,
        db: Session = Depends(dependencies.get_db),
):
    crud.delete_city(db=db, city_id=city_id)
    return CityDelete(deleted=True)
