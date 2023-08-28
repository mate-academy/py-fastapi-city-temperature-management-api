from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import cities.crud as crud
import cities.schemas as schemas
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="Such city already exists")

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Number of records to fetch"),
):
    return crud.read_all_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city_by_id(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_name(db=db, name=city_update.name)

    if not db_city:
        raise HTTPException(status_code=404, detail="Such city not found")

    return crud.update_city(db=db, city_id=city_id, city=city_update)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="Such city not found")

    return crud.delete_city(db=db, city=db_city)
