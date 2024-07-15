from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate, db: Session = Depends(get_db)
) -> schemas.City:
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=List[schemas.City])
def read_cities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[schemas.City]:
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.delete_city(db=db, city_id=city_id)
