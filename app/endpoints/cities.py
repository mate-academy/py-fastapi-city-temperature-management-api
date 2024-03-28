from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.crud.crud_cities import create_city, get_cities
from app.schemas.schemas import CityCreate, City

router = APIRouter()


@router.post("/cities/", response_model=City)
def create_city_endpoint(city: CityCreate, db: Session = Depends(get_db)) -> City:
    return create_city(db=db, city=city)


@router.get("/cities/", response_model=List[City])
def read_cities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[City]:
    cities = get_cities(db, skip=skip, limit=limit)
    return cities
