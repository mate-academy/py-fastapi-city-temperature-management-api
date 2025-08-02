from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from city_crud_api.schemas import CityCreate
from city_crud_api.schemas import City, CityUpdate
from city_crud_api.crud import (
    create_city as crud_create_city,
    get_cities,
    get_city_by_id as crud_get_city_by_id,
    crud_update_city,
    crud_delete_city
)
from dependencies import get_db

city_router = APIRouter()




@city_router.post("/cities/", response_model=City)
def create_city(
        city: CityCreate,
        db: Session = Depends(get_db)
):
    return crud_create_city(db=db, city=city)


@city_router.get("/cities/", response_model=list[City])
def list_cities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_cities(db=db, skip=skip, limit=limit)

@city_router.get("/cities/{city_id}", response_model=City)
def get_city_by_id(
    city_id: int,
    db: Session = Depends(get_db)
):
    db_city = crud_get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@city_router.put("/cities/{city_id}", response_model=City)
def update_city(
        city_id: int,
        city: CityUpdate,
        db: Session = Depends(get_db)
):
    db_city = crud_update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@city_router.delete("/cities/{city_id}")
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    db_city = crud_delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}

