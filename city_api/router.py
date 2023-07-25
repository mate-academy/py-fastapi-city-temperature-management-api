from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import City, CityCreate
from models import City as CityModel
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# POST /cities: Create a new city
@router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(SessionLocal)):
    try:
        db_city = CityModel(**city.dict())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")

# GET /cities: Get a list of all cities
@router.get("/cities/", response_model=List[City])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    cities = db.query(CityModel).offset(skip).limit(limit).all()
    return cities

# GET /cities/{city_id}: Get the details of a specific city
@router.get("/cities/{city_id}", response_model=City)
def get_city(city_id: int, db: Session = Depends(SessionLocal)):
    city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

# PUT /cities/{city_id}: Update the details of a specific city (Optional)
@router.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(SessionLocal)):
    try:
        db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        for key, value in city.dict().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
        return db_city
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")

# DELETE /cities/{city_id}: Delete a specific city
@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(SessionLocal)):
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
