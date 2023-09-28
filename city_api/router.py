from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

import database
from city_api import schemas, crud, models
from dependencies import get_db

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def list_cities(
        db: Session = Depends(get_db)
):
    return crud.get_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
def list_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city: models.DBCity,
        db: Session = Depends(get_db)
):
    db_city = crud.update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    del_city = crud.delete_city(db=db, city_id=city_id)
    if del_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return del_city
