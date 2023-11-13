from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city import schemas, crud, models
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.create_city(database=db, city=city)
    return db_city


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    return city


@router.get("/cities/", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(models.City).offset(skip).limit(limit).all()
    return cities


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id)
    return db_city
