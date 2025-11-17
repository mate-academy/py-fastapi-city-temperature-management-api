from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.city import CityCreate, City, CityUpdate
from app.crud.city import (
    create_city,
    get_cities,
    update_city,
    delete_city
)
from app.dependencies import get_city_or_404


router = APIRouter()

@router.post("/cities", response_model=City)
def city_create(
        city: CityCreate,
        db: Session = Depends(get_db)
) -> Any:
    return create_city(db, city)


@router.get("/cities", response_model=list[City])
def cities_get(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> Any:
    return get_cities(db, skip, limit)


@router.get("/cities/{city_id}", response_model=City)
def city_get(city: City = Depends(get_city_or_404)) -> Any:
    return city


@router.put("/cities/{city_id}", response_model=City)
def city_update(
        update: CityUpdate,
        db: Session = Depends(get_db),
        city=Depends(get_city_or_404)
) -> Any:
    updated = update_city(db, city.id, update)
    return updated


@router.delete("/cities/{city_id}")
def city_delete(
        db: Session = Depends(get_db),
        city=Depends(get_city_or_404)
) -> Any:
    delete_city(db, city.id)
    return {"status": "deleted"}
