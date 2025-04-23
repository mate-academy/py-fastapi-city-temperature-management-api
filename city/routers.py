from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import city.schemas, city.crud
from database import get_db

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

@router.post("/", response_model=city.schemas.City)
def create_city(city_data: city.schemas.CityCreate, db: Session = Depends(get_db)):
    return city.crud.create_city(db, city_data)

@router.get("/", response_model=list[city.schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return city.crud.get_cities(db)

@router.get("/{city_id}", response_model=city.schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = city.crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.put("/{city_id}", response_model=city.schemas.City)
def update_city(city_id: int, city: city.schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = city.crud.update_city(db, city_id, city)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = city.crud.delete_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}
