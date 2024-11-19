from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.city import CityCreate, CityUpdate, CityRead
from app.dependencies import get_db
from app.crud.city import (
    create_city,
    get_city_by_id,
    update_city,
    delete_city,
    get_cities
)

city_router = APIRouter()


@city_router.post("/cities", response_model=CityRead)
def create_city_endpoint(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db, city)


@city_router.get("/cities", response_model=list[CityRead])
def get_cities_endpoint(db: Session = Depends(get_db)):
    return get_cities(db)


@city_router.get("/cities/{city_id}", response_model=CityRead)
def get_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    return get_city_by_id(db, city_id)


@city_router.put("/cities/update/{city_id}", response_model=CityRead)
def update_city_endpoint(
        city_id: int, city: CityUpdate, db: Session = Depends(get_db)
):
    return update_city(db, city_id, city)


@city_router.delete("/cities/delete/{city_id}", status_code=204)
def delete_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    return delete_city(db, city_id)
