from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from . import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityDefault])
def get_all_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.CityDefault)
def create_city(new_city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, new_city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City with the same name already exists"
        )
    return crud.create_city(db, new_city)

