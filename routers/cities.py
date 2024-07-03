from typing import List

from app.crud import get_cities, delete_city
from app.schemas import City, CityCreate
from app.database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db=db, city=city)


@router.get("/cities/", response_model=List[City])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = get_cities(db, skip=skip, limit=limit)
    return cities


@router.delete("/cities/{city_id}", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city
