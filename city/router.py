from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from city import crud, schemas

router = APIRouter()


@router.post("/cities/", response_model=schemas.City, status_code=201)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
):
    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def get_all_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=schemas.City, status_code=200)
def get_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    db_city = crud.update_city(db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
