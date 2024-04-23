from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city_api import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityBase])
def read_all_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.post("/cities/", response_model=schemas.CityIn)
def add_city(
        city: schemas.CityIn,
        db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}")
def read_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city_by_id(db=db, city_id=city_id)


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city_by_id(db=db, city_id=city_id)
