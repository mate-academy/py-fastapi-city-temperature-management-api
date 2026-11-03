from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import City as CityModel
from app.schemas import City, CityCreate, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=City, status_code=201)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(CityModel).filter(CityModel.name == city.name).first()
    if db_city:
        raise HTTPException(status_code=400, detail="City with this name already exists")
    
    db_city = CityModel(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("/", response_model=List[City])
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(CityModel).all()
    return cities


@router.get("/{city_id}", response_model=City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=City)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    existing_city = db.query(CityModel).filter(
        CityModel.name == city.name, CityModel.id != city_id
    ).first()
    if existing_city:
        raise HTTPException(status_code=400, detail="City with this name already exists")
    
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db.delete(db_city)
    db.commit()
    return None
