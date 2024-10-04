from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.cities.models import City
from app.cities.schemas import CityCreate, CityOut
from app.database import get_db

router = APIRouter()

@router.post("/cities/", response_model=CityOut)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@router.get("/cities/", response_model=list[CityOut])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return cities

@router.delete("/cities/{city_id}", response_model=dict)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return {"detail": "City deleted"}

