from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud import city as city_crud
from app.schemas.city import City, CityCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return city_crud.create_city(db, city)


@router.get("/", response_model=List[City])
def get_cities(db: Session = Depends(get_db)):
    return city_crud.get_cities(db)
