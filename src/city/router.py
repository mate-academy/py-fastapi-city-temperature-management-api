from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies import get_db, common_parameters
from .dependencies import valid_city_id
from .schemas import City, CityCreate
from . import crud


router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=list[City])
def read_city_list(
    parameters: Annotated[dict, Depends(common_parameters)],
    db: Session = Depends(get_db),
):
    return crud.get_city_list(db, **parameters)


@router.get("/{city_id}/", response_model=City)
def read_city(city: City = Depends(valid_city_id)):
    return city


@router.post("/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city_data=city)


@router.put("/{city_id}/", response_model=CityCreate)
def update_city(
    city_data: CityCreate,
    city: City = Depends(valid_city_id),
    db: Session = Depends(get_db),
):
    return crud.update_city(db=db, city=city, city_data=city_data)


@router.delete("/{city_id}/", response_model=City)
def delete_city(city: City = Depends(valid_city_id), db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city=city)
