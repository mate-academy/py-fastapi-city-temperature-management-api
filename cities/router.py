from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud
router = APIRouter(prefix="/api")

@router.get("/cities", response_model=list[schemas.CitySchema])
def get_cities(db: Session = Depends(get_db),skip: int = 0, limit: int = 10):
    cities = crud.get_all_сities(db, skip, limit)
    return cities

@router.get("/cities/{city_id}", response_model=schemas.CitySchema)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.post("/cities", response_model=schemas.CitySchema)
def create_city(city: schemas.CityCreateSchema, db: Session = Depends(get_db)):
    return crud.create_city(db, city)

@router.put("/cities/{city_id}", response_model=schemas.CityCreateSchema)
def update_city(city_id: int, city: schemas.CityCreateSchema, db: Session = Depends(get_db)):
    return crud.update_city(db, city, city_id)

@router.delete("/cities/{city_id}", response_model=schemas.CitySchema) 
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db, city_id)