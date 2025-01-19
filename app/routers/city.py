from fastapi.exceptions import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.city import CityCreate
from app.crud.city import create_city, get_cities, get_city_by_id, update_city, delete_city
from app.database import SessionLocal
from app.models.city import City
from app.dependancies import get_db


router = APIRouter()


@router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db=db, city=city)


@router.get("/cities/", response_model=list[City])
def get_cities(db: Session = Depends(get_db)):
    return get_cities(db=db)


@router.get("/cities/{city_id}", response_model=list[City])
def get_cities_by_id(city_id: int, db: Session = Depends(get_db)):
    db_city = get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
