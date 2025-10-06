from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from city_temperature.database import get_db
from city_temperature.schemas import city as city_schema
from city_temperature.crud import city_crud

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=city_schema.City)
def create_city(city: city_schema.CityCreate, db: Session = Depends(get_db)):
    return city_crud.create_city(db=db, city=city)


@router.get("/", response_model=List[city_schema.City])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return city_crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=city_schema.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = city_crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=city_schema.City)
def update_city(city_id: int, city: city_schema.CityCreate, db: Session = Depends(get_db)):
    db_city = city_crud.update_city(db, city_id, city)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = city_crud.delete_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": f"City '{db_city.name}' deleted successfully"}
