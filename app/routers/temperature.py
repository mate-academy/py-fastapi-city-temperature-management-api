from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.temperature import Temperature
from app.crud.temperature import fetch_and_store_temperatures,get_temperatures, get_temperatures_by_city
from app.dependancies import get_db

router = APIRouter()


@router.post("/temperature/update/")
def update_temperatures(db: Session = Depends(get_db)):
    return fetch_and_store_temperatures(db=db)


@router.get("/temperature/", response_model=list[Temperature])
def get_temperatures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_temperatures(db=db, skip=skip, limit=limit)


@router.get("/temperature/by_city/{city_id}", response_model=list[Temperature])
def get_temperatures_by_city(city_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_temperatures_by_city(db=db, city_id=city_id, skip=skip, limit=limit)
