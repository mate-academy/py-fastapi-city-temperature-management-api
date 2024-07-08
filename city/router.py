from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from . import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities_list(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_city_by_id(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_city_by_id(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_city_by_id(db=db, city_id=city_id)
