from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from city import crud
from city.schemas import City, CityCreate, CityUpdate
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=List[City])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=City)
def create_city(city_in: CityCreate, db: Session = Depends(get_db)) -> City:
    return crud.create_city(db, city_in=city_in)


@router.put("/{city_id}", response_model=City)
def update_city(city_id: int,
                city_in: CityUpdate,
                db: Session = Depends(get_db)):
    db_city = crud.update_city(db, city_id=city_id, city_in=city_in)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    if not crud.delete_city(db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return None
