from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
import dependencies

router = APIRouter()


@router.post("/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate, db: Session = Depends(dependencies.get_db)
):
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=List[schemas.City])
def fetch_all_cities(
    commons: dependencies.CommonsDep,
    db: Session = Depends(dependencies.get_db),
):
    cities = crud.get_all_cities(db, commons["skip"], commons["limit"])
    return cities


@router.get("/{city_id}/", response_model=schemas.City)
def fetch_city_by_id(city_id: int, db: Session = Depends(dependencies.get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city


@router.put("/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(dependencies.get_db),
):
    db_city = crud.update_city(db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city


@router.delete("/{city_id}/", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(dependencies.get_db)):
    db_city = crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city
