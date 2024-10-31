from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, database

router = APIRouter()

@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(database.get_db)
):
    return crud.create_city(db=db, city=city)

@router.get("/cities/", response_model=List[schemas.City])
def read_cities(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(database.get_db)
):
    return crud.get_cities(db, skip=skip, limit=limit)

@router.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_city(db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return
