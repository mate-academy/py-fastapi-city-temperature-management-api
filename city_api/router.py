from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from dependencies import get_db
from city_api.schemas import City, CityCreate
from city_api.models import City as CityModel


city_router = APIRouter()


@city_router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    try:
        db_city = CityModel(**city.model_dump())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")


@city_router.get("/cities/", response_model=List[City])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = db.query(CityModel).offset(skip).limit(limit).all()
    return cities


@city_router.get("/cities/{city_id}", response_model=City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@city_router.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    try:
        db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        for key, value in city.model_dump().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
        return db_city
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")


@city_router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    try:
        db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        db.delete(db_city)
        db.commit()
        return {"message": "City deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")
