from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from city import crud, schemas
from db.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.CityList])
def read_cities(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> schemas.CityList:
    cities = crud.get_all_city(db=db)
    return cities


@router.post("/", response_model=schemas.CityList)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)) -> Any:
    db_city = crud.create_city(db, city)
    if db_city is None:
        raise HTTPException(
            status_code=400,
            detail="Such name and additional info for city already exists",
        )
    return db_city


@router.get("/{city_id}", response_model=schemas.CityList)
def read_city(
    city_id: int, db: Session = Depends(get_db)
) -> schemas.CityList:
    db_city = crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", response_model=schemas.CityList)
def delete_city(
    city_id: int, db: Session = Depends(get_db)
) -> schemas.CityList:
    db_city = crud.delete_city_by_id(db, city_id)
    if isinstance(db_city, HTTPException):
        raise db_city
    return db_city
