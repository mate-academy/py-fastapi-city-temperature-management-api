from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityResponse])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/cities/", response_model=schemas.CityResponse)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.CityResponse)
def update_city(
        city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)
):
    updated_city = crud.update_city(db=db, city_id=city_id, city_update=city)

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not Found")

    return updated_city


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = crud.delete_city(db=db, city_id=city_id)

    if deleted_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return {"message": "City deleted successfully"}
